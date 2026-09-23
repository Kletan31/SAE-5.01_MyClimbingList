# ===============================================================
# Command : Génération du cache de fréquentation réelle (14 j)
# ===============================================================

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
import plotly.graph_objects as go
import os

from django.contrib.auth import get_user_model
from applications.core.models.seance import Seance
from applications.contest.models.contest_result import ContestResult

User = get_user_model()

# === Constantes === #
SALLE_NAMES = {
    3: "Montaudran", 4: "Albi", 5: "Grabels", 7: "Saint-Martin",
    9: "Odysseum", 10: "Marseille", 12: "Nantes", 14: "Metz",
    15: "Perpignan", 18: "Portet", 19: "Loisirama", 100: "Lisboa",
}

CACHE_DIR = "cache/dir_admin"
GLOBAL_CACHE_FILE = os.path.join(CACHE_DIR, "frequentation.html")
SALLE_CACHE_DIR = os.path.join(CACHE_DIR, "frequentation_salles")


class Command(BaseCommand):
    help = "Génère et met en cache les graphes de fréquentation réelle pour la direction et chaque salle"

    def handle(self, *args, **kwargs):
        print("=== Génération du cache de fréquentation réelle... ===")

        today = now().date()
        first_seance = Seance.objects.order_by("date_seance").first()
        if not first_seance:
            print("Aucune séance enregistrée, arrêt du script.")
            return

        start_date = first_seance.date_seance
        end_date = today - timedelta(days=1)
        total_days = (end_date - start_date).days
        future_buffer = timedelta(days=int(total_days * 0.1))

        # =====================================================
        #  Pré-calcul : user -> dernière salle connue
        # =====================================================
        user_last_salle = (
            Seance.objects.values("user", "ouverture__salle_id", "date_seance")
            .order_by("user", "-date_seance")
        )

        last_seen = {}
        for record in user_last_salle:
            uid = record["user"]
            if uid not in last_seen:  # on garde uniquement la plus récente
                last_seen[uid] = record["ouverture__salle_id"]

        # =====================================================
        #  Initialisation
        # =====================================================
        global_dates = []
        global_values = []
        salle_series = {salle_id: [] for salle_id in SALLE_NAMES}

        # =====================================================
        #  Boucle jour par jour
        # =====================================================
        current_day = start_date
        while current_day <= end_date:
            window_start = current_day - timedelta(days=13)

            # --- Utilisateurs avec activité réelle (séance ou contest)
            seance_users = set(
                Seance.objects.filter(
                    date_seance__range=(window_start, current_day)
                ).values_list("user", flat=True)
            )

            contest_users = set(
                ContestResult.objects.filter(
                    created_at__date__range=(window_start, current_day)
                ).values_list("user", flat=True)
            )

            # --- Utilisateurs avec last_login récent
            login_users = set(
                User.objects.filter(
                    last_login__date__range=(window_start, current_day)
                ).values_list("id", flat=True)
            )

            # --- Exclure ceux sans salle (aucune séance ni contest jamais associé)
            known_users = set(last_seen.keys())
            login_users_with_activity = login_users.intersection(known_users)

            # --- Ensemble final des utilisateurs actifs
            active_users = seance_users.union(contest_users, login_users_with_activity)

            # --- Total global
            global_dates.append(current_day)
            global_values.append(len(active_users))

            # --- Répartition par salle
            salle_counts = {sid: 0 for sid in SALLE_NAMES}
            for uid in active_users:
                salle_id = last_seen.get(uid)
                if salle_id in salle_counts:
                    salle_counts[salle_id] += 1

            for sid in SALLE_NAMES:
                salle_series[sid].append(salle_counts[sid])

            current_day += timedelta(days=1)

        # =====================================================
        #  Création des graphiques Plotly
        # =====================================================

        # --- Graphique global ---
        fig_global = go.Figure()
        fig_global.add_trace(go.Scatter(
            x=global_dates, y=global_values,
            mode="lines",
            name="Utilisateurs actifs (14 j glissants)",
            line=dict(color="#4CAF50", width=2),
        ))
        fig_global.update_layout(
            title="Fréquentation réelle – toutes salles confondues",
            xaxis_title="Date",
            yaxis_title="Utilisateurs actifs",
            template="plotly_white",
            height=450,
            xaxis=dict(range=[global_dates[0], end_date + future_buffer]),
        )

        # --- Graphique par salle ---
        fig_salle = go.Figure()
        for salle_id, y_values in salle_series.items():
            fig_salle.add_trace(go.Scatter(
                x=global_dates, y=y_values,
                mode="lines",
                name=SALLE_NAMES[salle_id],
            ))
        fig_salle.update_layout(
            title="Fréquentation réelle par salle",
            xaxis_title="Date",
            yaxis_title="Utilisateurs actifs",
            template="plotly_white",
            height=550,
            xaxis=dict(range=[global_dates[0], end_date + future_buffer]),
        )

        # =====================================================
        #  Sauvegarde des fichiers HTML dans le cache
        # =====================================================
        os.makedirs(CACHE_DIR, exist_ok=True)
        os.makedirs(SALLE_CACHE_DIR, exist_ok=True)

        # Sauvegarde du fichier global combiné (global + par salle)
        with open(GLOBAL_CACHE_FILE, "w") as f:
            f.write(fig_global.to_html(full_html=False))
            f.write("<hr>")
            f.write(fig_salle.to_html(full_html=False))

        # Sauvegarde des fichiers individuels par salle
        for salle_id, y_values in salle_series.items():
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=global_dates, y=y_values,
                mode="lines",
                name=SALLE_NAMES[salle_id],
            ))
            fig.update_layout(
                title=f"Fréquentation réelle – {SALLE_NAMES[salle_id]}",
                xaxis_title="Date",
                yaxis_title="Utilisateurs actifs",
                template="plotly_white",
                height=450,
                xaxis=dict(range=[global_dates[0], end_date + future_buffer]),
            )

            salle_file = os.path.join(SALLE_CACHE_DIR, f"{salle_id}.html")
            with open(salle_file, "w") as f:
                f.write(fig.to_html(full_html=False))

        print(f"Graphiques générés et enregistrés dans :\n"
              f" - {GLOBAL_CACHE_FILE}\n"
              f" - {SALLE_CACHE_DIR}/<salle_id>.html")
