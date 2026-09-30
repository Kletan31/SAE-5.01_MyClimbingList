from django.core.management.base import BaseCommand
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
import plotly.graph_objects as go
import os
from django.contrib.auth import get_user_model
from django.db.models import F, ExpressionWrapper, DurationField


User = get_user_model()

CACHE_DIR = "cache/dir_admin"
RETENTION_CACHE_FILE = os.path.join(CACHE_DIR, "retention.html")


class Command(BaseCommand):
    help = "Génère et met en cache le graphique de rétention à 1 an"

    def handle(self, *args, **kwargs):
        print("Génération du graphique de rétention à 1 an...")

        now = timezone.now().date()
        one_year = timedelta(days=365)
        two_weeks = timedelta(days=14)

        labels = []
        total_list = []
        retained_list = []

        for i in range(365, -1, -1):
            ref_date = now - timedelta(days=i)
            ref_datetime = timezone.make_aware(datetime.combine(ref_date, datetime.min.time()))
            one_year_ago = ref_datetime - one_year

            # Utilisateurs inscrits depuis plus d'un an
            old_users = User.objects.filter(date_joined__lte=one_year_ago)
            total = old_users.count()

            # Toujours actifs ≥ 365 j après inscription
            eligible = old_users.filter(last_login__isnull=False).annotate(
                delta=ExpressionWrapper(
                    F("last_login") - F("date_joined"),
                    output_field=DurationField()
                )
            ).filter(delta__gte=one_year).count()

            labels.append(ref_date.strftime("%Y-%m-%d"))
            total_list.append(total)
            retained_list.append(eligible)

        # === Création du graphique === #
        fig = go.Figure()

        # --- Total inscrits depuis > 1 an ---
        fig.add_trace(go.Scatter(
            x=labels, y=total_list,
            mode="lines",
            name="Utilisateurs inscrits depuis > 1 an",
            line=dict(color="#8884d8", width=2),
            hovertemplate="%{y}<extra></extra>",
        ))

        # --- Toujours actifs ≥ 1 an après inscription ---
        fig.add_trace(go.Scatter(
            x=labels, y=retained_list,
            mode="lines",
            name="Toujours actifs un an après inscription",
            line=dict(color="#4CAF50", width=2),
            hovertemplate="%{y}<extra></extra>",
        ))

        # --- Mise en forme ---
        fig.update_layout(
            title="Évolution du taux de rétention à 1 an",
            xaxis_title="Date",
            yaxis_title="Nombre d’utilisateurs",
            template="plotly_white",
            legend=dict(yanchor="top", y=1, xanchor="left", x=0),
            margin=dict(l=40, r=40, t=80, b=40),
            height=550,
        )

        # === Sauvegarde du cache === #
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(RETENTION_CACHE_FILE, "w") as f:
            f.write(fig.to_html(full_html=False))

        print(f"Graphique de rétention mis en cache : {RETENTION_CACHE_FILE}")
