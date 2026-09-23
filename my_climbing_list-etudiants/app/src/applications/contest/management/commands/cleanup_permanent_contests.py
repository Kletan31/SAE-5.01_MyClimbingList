# applications/contest/management/commands/cleanup_permanent_contests.py

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Max
from django.utils import timezone

from applications.contest.models import Contest, Inscription
from applications.core.models import Seance
from applications.contest.utils.scoring import compute_permanent_success


def get_relais_en_tete_for(contest: Contest) -> list[int]:
    """
    Renvoie la liste des relais où 'tête' est imposé pour ce contest.
    Fallback sûr : liste vide = 'tête' non imposé.
    """
    try:
        return list(getattr(contest.salle, "relais_en_tete", []) or [])
    except Exception:
        return []


class Command(BaseCommand):
    help = (
        "Nettoie les contests PERMANENTS : désinscrit les utilisateurs qui ont 0 point "
        "et aucune séance depuis N jours (par défaut 14). "
        "COMMIT par défaut — utiliser --dry-run pour tester."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="Seuil d'inactivité en jours (default: 14).",
        )
        parser.add_argument(
            "--contest-id",
            type=int,
            help="Limiter au contest spécifié (ID).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mode simulation (aucune suppression).",
        )

    def handle(self, *args, **opts):
        days = opts["days"]
        dry_run = opts["dry_run"]
        contest_id = opts.get("contest_id")

        commit = not dry_run
        cutoff = timezone.now() - timedelta(days=days)

        self.stdout.write(
            f"[cleanup_permanent_contests] mode={'COMMIT' if commit else 'DRY-RUN'} | "
            f"days={days} | cutoff={cutoff:%Y-%m-%d %H:%M}"
        )

        contests = Contest.objects.filter(
            is_permanent=True,
            is_permanent_enabled=True,
            is_active=True,
        )

        if contest_id:
            contests = contests.filter(pk=contest_id)

        total_checked = 0
        total_removed = 0

        for contest in contests:
            self.stdout.write(self.style.HTTP_INFO(
                f"→ Contest #{contest.id} · {contest.name}"
            ))

            inscriptions = (
                Inscription.objects
                .filter(contest=contest)
                .select_related("user")
            )

            inscrit_ids = list(inscriptions.values_list("user_id", flat=True))
            if not inscrit_ids:
                self.stdout.write("  (aucune inscription)")
                continue

            ouverture_ids = list(contest.ouvertures.values_list("id", flat=True))
            if not ouverture_ids:
                self.stdout.write("  (aucune ouverture liée)")
                continue

            relais_en_tete = get_relais_en_tete_for(contest)

            # 1️⃣ Succès (source de vérité)
            _, openings_by_user = compute_permanent_success(
                contest=contest,
                inscrit_ids=inscrit_ids,
                ouverture_ids=ouverture_ids,
                relais_en_tete=relais_en_tete,
            )
            users_with_success = set(openings_by_user.keys())

            # 2️⃣ Dernière séance (created_at)
            last_sessions = (
                Seance.objects
                .filter(
                    user_id__in=inscrit_ids,
                    ouverture_id__in=ouverture_ids,
                )
                .values("user_id")
                .annotate(last_ts=Max("created_at"))
            )
            last_by_user = {row["user_id"]: row["last_ts"] for row in last_sessions}

            to_remove = []

            for ins in inscriptions:
                total_checked += 1
                uid = ins.user_id

                has_points = uid in users_with_success
                last_ts = last_by_user.get(uid)
                inactive = (last_ts is None) or (last_ts < cutoff)

                should_remove = (not has_points) and inactive

                self.stdout.write(
                    f"  - {ins.user} | "
                    f"pts={'YES' if has_points else 'NO'} | "
                    f"last={last_ts or '—'} | "
                    f"remove={should_remove}"
                )

                if should_remove:
                    to_remove.append(ins)

            if not to_remove:
                self.stdout.write("  Aucun inscrit à supprimer.")
                continue

            if commit:
                ids = [i.pk for i in to_remove]
                deleted, _ = Inscription.objects.filter(pk__in=ids).delete()
                total_removed += deleted
                self.stdout.write(self.style.SUCCESS(f"  Supprimés: {deleted}"))
            else:
                self.stdout.write(self.style.WARNING(
                    f"  (DRY-RUN) À supprimer: {len(to_remove)}"
                ))

        summary = (
            f"Checked={total_checked} | Removed={total_removed} | "
            f"Mode={'COMMIT' if commit else 'DRY-RUN'}"
        )

        if commit:
            self.stdout.write(self.style.SUCCESS(summary))
        else:
            self.stdout.write(self.style.WARNING(summary))
