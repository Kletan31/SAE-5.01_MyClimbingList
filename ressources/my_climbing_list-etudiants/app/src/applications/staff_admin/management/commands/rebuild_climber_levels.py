# applications/core/management/commands/rebuild_climber_levels.py

from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Min
from django.contrib.auth import get_user_model

from applications.core.models import Seance
from applications.staff_admin.models import ClimberLevelDaily
from applications.staff_admin.utils import (
    initial_elo_state,
    compute_day,
    elo_to_level_and_color,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Rebuild ClimberLevelDaily from Seance history"

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-date",
            type=str,
            help="Force rebuild starting from YYYY-MM-DD",
        )
        parser.add_argument(
            "--user-id",
            type=int,
            help="Rebuild only for one user",
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")
        forced_from_date = options.get("from_date")

        start_date = self._get_start_date(forced_from_date, user_id)
        if not start_date:
            self.stdout.write(self.style.WARNING("No rebuild needed."))
            return

        today = date.today()

        self.stdout.write(
            self.style.NOTICE(
                f"Rebuilding ClimberLevelDaily from {start_date} to {today}"
            )
        )

        with transaction.atomic():
            self._cleanup(start_date, user_id)
            self._rebuild(start_date, today, user_id)

        self.stdout.write(self.style.SUCCESS("Rebuild complete."))

    # -----------------------------------------------------
    # DATE LOGIC
    # -----------------------------------------------------

    def _get_start_date(self, forced_from_date, user_id):
        if forced_from_date:
            return date.fromisoformat(forced_from_date)

        qs = Seance.objects.all()
        if user_id:
            qs = qs.filter(user_id=user_id)

        return qs.aggregate(Min("date_seance"))["date_seance__min"]

    # -----------------------------------------------------
    # CLEANUP
    # -----------------------------------------------------

    def _cleanup(self, start_date, user_id):
        qs = ClimberLevelDaily.objects.filter(date__gte=start_date)
        if user_id:
            qs = qs.filter(user_id=user_id)

        deleted, _ = qs.delete()
        self.stdout.write(f"Deleted {deleted} ClimberLevelDaily rows")

    # -----------------------------------------------------
    # REBUILD LOOP WITH PROGRESS
    # -----------------------------------------------------

    def _rebuild(self, start_date, end_date, user_id):
        users = list(self._get_users(user_id))
        total_users = len(users)

        for index, user in enumerate(users, start=1):
            self.stdout.write(
                self.style.NOTICE(
                    f"[{index}/{total_users}] User {user.username} (id={user.id})"
                )
            )

            for bloc in (True, False):
                discipline = "Bloc" if bloc else "Voie"
                self.stdout.write(f"  - {discipline} : rebuild started")
                self._rebuild_user_bloc(user, bloc, start_date, end_date)
                self.stdout.write(f"  - {discipline} : done")

    def _rebuild_user_bloc(self, user, bloc, start_date, end_date):
        state = initial_elo_state()
        current_day = start_date

        while current_day <= end_date:
            state = compute_day(
                user=user,
                bloc=bloc,
                day=current_day,
                state=state,
            )

            if state["elo"] is not None:
                level, color = elo_to_level_and_color(state["elo"])
                ClimberLevelDaily.objects.create(
                    user=user,
                    bloc=bloc,
                    date=current_day,
                    elo=state["elo"],
                    level=level,
                    color=color,
                )

            current_day += timedelta(days=1)

    # -----------------------------------------------------
    # UTILS
    # -----------------------------------------------------

    def _get_users(self, user_id):
        qs = User.objects.filter(seance__isnull=False).distinct()
        if user_id:
            qs = qs.filter(id=user_id)
        return qs
