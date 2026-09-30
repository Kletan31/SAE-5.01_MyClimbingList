from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from applications.staff_admin.models import ClimberLevelDaily

User = get_user_model()


class Command(BaseCommand):
    help = "Compute elo_trend for ClimberLevelDaily rows"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            help="Compute trends only for one user",
        )
        parser.add_argument(
            "--window-days",
            type=int,
            default=7,
            help="Number of days to look back (default: 7)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Display detailed per-user logs",
        )

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def handle(self, *args, **options):
        user_id = options.get("user_id")
        window_days = options["window_days"]
        verbose = options["verbose"]

        qs = ClimberLevelDaily.objects.all()

        if user_id:
            qs = qs.filter(user_id=user_id)

        qs = qs.order_by("user_id", "bloc", "date")

        total_users = qs.values("user_id").distinct().count()

        if verbose:
            self.stdout.write(
                self.style.NOTICE(
                    f"Computing elo_trend (window={window_days} days) "
                    f"for {total_users} user(s)"
                )
            )

        with transaction.atomic():
            self._compute(
                qs,
                window_days=window_days,
                total_users=total_users,
                verbose=verbose,
            )

        if verbose:
            self.stdout.write(self.style.SUCCESS("elo_trend computation complete."))

    # =====================================================
    # CORE LOGIC
    # =====================================================

    def _compute(self, qs, window_days, total_users, verbose=False):
        current_key = None
        history = []

        current_user_id = None
        user_index = 0

        for row in qs:
            key = (row.user_id, row.bloc)

            # Changement d'utilisateur
            if row.user_id != current_user_id:
                current_user_id = row.user_id
                user_index += 1

                if verbose:
                    self.stdout.write(
                        self.style.NOTICE(
                            f"[{user_index}/{total_users}] "
                            f"User {row.user.username} (id={row.user_id})"
                        )
                    )

            # Changement bloc / voie
            if key != current_key:
                current_key = key
                history = []

                if verbose:
                    discipline = "Bloc" if row.bloc else "Voie"
                    self.stdout.write(f"  - {discipline}")

            trend = self._compute_trend_for_row(row, history, window_days)

            row.elo_trend = trend
            row.save(update_fields=["elo_trend"])

            history.append({
                "date": row.date,
                "elo": row.elo,
            })

    # =====================================================
    # TREND LOGIC
    # =====================================================

    def _compute_trend_for_row(self, row, history, window_days):
        if not history:
            return None

        current = row.elo
        if current is None:
            return None

        limit_date = row.date - timedelta(days=window_days)

        previous = None

        for h in reversed(history):
            d = h.get("date")
            e = h.get("elo")

            if d is None or d < limit_date:
                break

            if e is None:
                continue

            if e != current:
                previous = e
                break

        if previous is None:
            return None

        delta = current - previous

        if abs(delta) <= 1:
            return None

        return "up" if delta > 0 else "down"
