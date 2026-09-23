# applications/custom_auth/management/commands/assign_user_salle.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Count

from applications.custom_auth.models import Salle
from applications.core.models import Seance, Ouverture

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Associe une salle VOIE et une salle BLOC à chaque utilisateur non-staff "
        "en fonction de son activité réelle."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Affiche les résultats sans modifier la base",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        self.stdout.write(self.style.MIGRATE_HEADING(
            "→ Attribution des salles utilisateurs (voie / bloc)"
        ))

        # --------------------------------------------------
        # Utilisateurs concernés
        # --------------------------------------------------
        users = (
            User.objects
            .filter(is_staff=False, is_superuser=False)
            .select_related("profile")
        )

        self.stdout.write(f"Utilisateurs analysés : {users.count()}")

        updated = 0

        # --------------------------------------------------
        # Pré-calcul : ouvertures actives par salle & discipline
        # --------------------------------------------------
        def get_active_openings_by_salle(bloc: bool) -> dict[int, int]:
            return dict(
                Ouverture.objects
                .filter(active=True, bloc=bloc)
                .values("salle_id")
                .annotate(count=Count("id"))
                .values_list("salle_id", "count")
            )

        active_openings_voie = get_active_openings_by_salle(bloc=False)
        active_openings_bloc = get_active_openings_by_salle(bloc=True)

        if not active_openings_voie and not active_openings_bloc:
            self.stdout.write(self.style.WARNING(
                "Aucune ouverture active trouvée (voie ou bloc)."
            ))
            return

        # --------------------------------------------------
        # Fonction générique de calcul de meilleure salle
        # --------------------------------------------------
        def compute_best_salle(user, bloc: bool, active_openings: dict[int, int]):
            essais_par_salle = dict(
                Seance.objects
                .filter(
                    user=user,
                    ouverture__active=True,
                    ouverture__bloc=bloc,
                    ouverture__salle__isnull=False,
                )
                .values("ouverture__salle_id")
                .annotate(count=Count("id"))
                .values_list("ouverture__salle_id", "count")
            )

            best_salle_id = None
            best_score = 0.0

            for salle_id, nb_essais in essais_par_salle.items():
                nb_ouvertures = active_openings.get(salle_id)
                if not nb_ouvertures:
                    continue

                score = nb_essais / nb_ouvertures

                if score > best_score:
                    best_score = score
                    best_salle_id = salle_id

            return best_salle_id, best_score

        # --------------------------------------------------
        # Boucle utilisateur
        # --------------------------------------------------
        for user in users:
            profile = getattr(user, "profile", None)
            if not profile:
                continue

            # ---------- VOIE ----------
            salle_voie_id, score_voie = compute_best_salle(
                user,
                bloc=False,
                active_openings=active_openings_voie,
            )

            # ---------- BLOC ----------
            salle_bloc_id, score_bloc = compute_best_salle(
                user,
                bloc=True,
                active_openings=active_openings_bloc,
            )

            fields_to_update = []

            if salle_voie_id and profile.salle_voie_id != salle_voie_id:
                profile.salle_voie_id = salle_voie_id
                fields_to_update.append("salle_voie")

            if salle_bloc_id and profile.salle_bloc_id != salle_bloc_id:
                profile.salle_bloc_id = salle_bloc_id
                fields_to_update.append("salle_bloc")

            if fields_to_update:
                updated += 1

                if not dry_run:
                    profile.save(update_fields=fields_to_update)

                log_parts = []
                if salle_voie_id:
                    log_parts.append(f"voie={Salle.objects.get(id=salle_voie_id).nom} ({score_voie:.3f})")
                if salle_bloc_id:
                    log_parts.append(f"bloc={Salle.objects.get(id=salle_bloc_id).nom} ({score_bloc:.3f})")

                self.stdout.write(
                    f"✔ {user.username} → " + " | ".join(log_parts)
                )

        if dry_run:
            self.stdout.write(
                self.style.WARNING("Mode dry-run : aucune modification appliquée.")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Salles mises à jour : {updated}")
        )
