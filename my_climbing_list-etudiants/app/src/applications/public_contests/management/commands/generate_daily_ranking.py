# applications/public_contests/management/commands/generate_daily_ranking.py

from datetime import timedelta
from pathlib import Path

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.timezone import localdate

from django.contrib.staticfiles.storage import (
    staticfiles_storage,
    StaticFilesStorage,
)

from applications.staff_admin.models import ClimberLevelDaily
from applications.core.models import Seance


CACHE_DIR = Path("cache/public_contests")


def compute_total_successes(user, bloc: bool):
    """
    Nombre de succès DISTINCTS pour une discipline donnée (voie / bloc).
    La règle tête / moulinette dépend de la salle de l'ouverture.
    """

    seances = (
        Seance.objects
        .filter(
            user=user,
            ouverture__bloc=bloc,
        )
        .select_related("ouverture", "ouverture__salle")
    )

    successful_openings = set()

    for seance in seances:
        ouverture = seance.ouverture
        salle = ouverture.salle

        if not salle:
            continue

        relais = ouverture.relais
        relais_en_tete = salle.relais_en_tete or []

        # Tête si autorisée sur ce relais, sinon moulinette
        if relais in relais_en_tete:
            if seance.nb_top_lead > 0:
                successful_openings.add(ouverture.id)
        else:
            if seance.nb_top > 0:
                successful_openings.add(ouverture.id)

    return len(successful_openings)


class Command(BaseCommand):
    help = "Génère le classement Elo public journalier (HTML statique)"

    def handle(self, *args, **options):
        # =====================================================
        # Fenêtre temporelle
        # =====================================================
        today = localdate() - timedelta(days=1)
        since = today - timedelta(days=30)

        self.stdout.write("→ Génération du classement Alti Ligue")

        # =====================================================
        # Préparation cache + static
        # =====================================================
        staticfiles_storage._wrapped = StaticFilesStorage()
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # =====================================================
        # Utilisateurs actifs sur les 30 derniers jours
        # =====================================================
        active_user_ids = (
            Seance.objects
            .filter(date_seance__gte=since)
            .values_list("user_id", flat=True)
            .distinct()
        )

        # =====================================================
        # Génération pour voie et bloc
        # =====================================================
        for bloc in (False, True):

            qs = (
                ClimberLevelDaily.objects
                .filter(
                    date=today,
                    bloc=bloc,
                    elo__isnull=False,
                    user_id__in=active_user_ids,
                )
                .select_related(
                    "user",
                    "user__profile",
                    "user__profile__favorite_salle",
                    "user__profile__salle_voie",
                    "user__profile__salle_bloc",
                )
                .order_by("-elo")[:100]
            )

            climbers = []

            for row in qs:
                user = row.user
                profile = getattr(user, "profile", None)

                # ---------------------------------------------
                # Détermination des salles affichées
                # ---------------------------------------------
                salle_voie = None
                salle_bloc = None

                salle_voie = profile.favorite_salle or profile.salle_voie
                salle_bloc = profile.favorite_salle or profile.salle_bloc

                salle_display = salle_bloc if bloc else salle_voie

                # ---------------------------------------------
                # EXCLUSION : pas de salle définie
                # ---------------------------------------------
                if salle_display is None:
                    continue

                # ---------------------------------------------
                # Stats
                # ---------------------------------------------
                total_successes = compute_total_successes(user, bloc)

                climbers.append({
                    "user": user,
                    "elo": row.elo,
                    "level": row.level,
                    "color": row.color,
                    "elo_trend": row.elo_trend,
                    "salle": salle_display,
                    "successes": total_successes,
                })

            # =====================================================
            # Rendu HTML
            # =====================================================
            context = {
                "climbers": climbers,
                "bloc": bloc,
                "date": today,
                "limit": 100,
                "since": since,
            }

            html = render_to_string(
                "public_contests/climber_ranking/climber_ranking.html",
                context,
            )

            filename = (
                "climber_ranking_bloc.html"
                if bloc else
                "climber_ranking_voie.html"
            )

            (CACHE_DIR / filename).write_text(html, encoding="utf-8")

            self.stdout.write(
                self.style.SUCCESS(
                    f"✔ {filename} généré ({len(climbers)} grimpeurs)"
                )
            )

        self.stdout.write(self.style.SUCCESS("✓ Classement Alti Ligue prêt"))
