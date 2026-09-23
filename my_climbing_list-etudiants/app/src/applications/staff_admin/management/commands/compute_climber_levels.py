from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max, Min
from django.contrib.auth import get_user_model

from applications.core.models import Seance
from applications.staff_admin.models import ClimberLevelDaily
from applications.staff_admin.utils import (
    initial_elo_state,
    compute_day,
    elo_to_level_and_color,
)
from applications.staff_admin.management.commands.compute_elo_trends import (
    Command as TrendCommand,
)
from applications.staff_admin.utils.elo_engine import NIVEAU_PATTERN

User = get_user_model()


class Command(BaseCommand):
    help = "Daily incremental computation of ClimberLevelDaily (meant to run at 04:00)"

    # ==================================================
    # Entry point
    # ==================================================

    def handle(self, *args, **options):
        today = date.today()
        target_day = today - timedelta(days=1)

        self.stdout.write(f"Daily Elo computation for {target_day}")

        # ==================================================
        # 1) Last complete day
        # ==================================================

        last_complete_day = self._get_last_complete_day()
        start_day = (
            target_day
            if last_complete_day is None
            else last_complete_day + timedelta(days=1)
        )

        if start_day > target_day:
            self.stdout.write(self.style.WARNING("Nothing to compute."))
            return

        # ==================================================
        # 2) Base impacted users (existing Elo users)
        # ==================================================

        impacted = {
            user_id: start_day
            for user_id in
            ClimberLevelDaily.objects.values_list("user_id", flat=True).distinct()
        }

        # ==================================================
        # 3) Past modifications
        # ==================================================

        past_modifs = self._detect_impacted_users(target_day)
        for user_id, modif_start in past_modifs.items():
            impacted[user_id] = min(
                impacted.get(user_id, modif_start),
                modif_start,
            )

        # ==================================================
        # 4) Newly eligible users
        # ==================================================

        newly_eligible = self._detect_newly_eligible_users(target_day)
        for user_id, start_date in newly_eligible.items():
            impacted[user_id] = min(
                impacted.get(user_id, start_date),
                start_date,
            )

        impacted = {
            user_id: start_date
            for user_id, start_date in impacted.items()
            if start_date <= target_day
        }

        total_users = len(impacted)

        self.stdout.write(
            self.style.NOTICE(
                f"Rebuilding Elo for {total_users} users "
                f"from {start_day} to {target_day}"
            )
        )

        # ==================================================
        # EXECUTION (Elo computation)
        # ==================================================

        user_logs = {}

        with transaction.atomic():
            for idx, (user_id, start_date) in enumerate(impacted.items(), start=1):
                user = User.objects.get(id=user_id)

                log = {
                    "user": user,
                    "is_new": user_id in newly_eligible,
                    "rebuild_from": (
                        start_date if start_date < target_day else None
                    ),
                    "had_activity": Seance.objects.filter(
                        user=user,
                        date_seance=target_day,
                    ).exists(),
                    "elo_before": None,
                    "elo_after": None,
                }

                log["elo_before"] = (
                    ClimberLevelDaily.objects
                    .filter(user=user, date=target_day - timedelta(days=1))
                    .aggregate(Max("elo"))["elo__max"]
                )

                self._cleanup_user(user, start_date)
                self._compute_user(user, start_date, target_day)

                log["elo_after"] = (
                    ClimberLevelDaily.objects
                    .filter(user=user, date=target_day)
                    .aggregate(Max("elo"))["elo__max"]
                )

                user_logs[user_id] = log

        # ==================================================
        # DISPLAY (one line per user)
        # ==================================================

        for idx, log in enumerate(user_logs.values(), start=1):
            user = log["user"]
            status = "NEW" if log["is_new"] else "EXISTING"

            if log["rebuild_from"]:
                action = f"REBUILD from {log['rebuild_from']}"
            elif log["had_activity"]:
                before = log["elo_before"] or 0
                after = log["elo_after"] or before
                delta = int(after - before)
                sign = "+" if delta >= 0 else ""
                action = f"ACTIVE ({sign}{delta})"
            else:
                action = "AUTO"

            self.stdout.write(
                f"[{idx}/{total_users}] "
                f"{user.username} (id={user.id}) | {status} | {action}"
            )

        # ==================================================
        # Trends (logs handled here)
        # ==================================================

        self.stdout.write("Calcul des trends en cours...")

        self._compute_trends(impacted)

        self.stdout.write(self.style.SUCCESS("Calcul des trends terminé."))
        self.stdout.write(self.style.SUCCESS("Daily Elo update complete."))

    # ==================================================
    # Helpers (unchanged)
    # ==================================================

    def _get_last_complete_day(self):
        qs = (
            ClimberLevelDaily.objects
            .values("user_id", "bloc")
            .annotate(last_day=Max("date"))
        )
        if not qs.exists():
            return None
        return min(row["last_day"] for row in qs)

    def _detect_impacted_users(self, target_day):
        last_complete = self._get_last_complete_day()
        if not last_complete:
            return {}

        qs = (
            Seance.objects
            .filter(
                updated_at__date__gt=last_complete,
                date_seance__lte=target_day,
            )
            .values("user_id")
            .annotate(min_date=Min("date_seance"))
        )
        return {row["user_id"]: row["min_date"] for row in qs}

    def _detect_newly_eligible_users(self, target_day):
        impacted = {}

        active_users = (
            Seance.objects
            .filter(date_seance=target_day)
            .values_list("user_id", flat=True)
            .distinct()
        )

        users_with_elo = set(
            ClimberLevelDaily.objects
            .values_list("user_id", flat=True)
            .distinct()
        )

        for user_id in set(active_users) - users_with_elo:
            user = User.objects.get(id=user_id)
            for bloc in (True, False):
                eligible, start_date = self._is_user_elo_eligible(
                    user, bloc, target_day
                )
                if eligible:
                    impacted[user_id] = start_date
                    break

        return impacted

    def _is_user_elo_eligible(self, user, bloc, target_day):
        first_seance = (
            Seance.objects
            .filter(
                user=user,
                ouverture__bloc=bloc,
                ouverture__niveau__regex=NIVEAU_PATTERN,
                date_seance__lte=target_day,
            )
            .order_by("date_seance", "created_at")
            .first()
        )

        if not first_seance:
            return False, None

        state = initial_elo_state()
        current_day = first_seance.date_seance

        while current_day <= target_day:
            state = compute_day(
                user=user,
                bloc=bloc,
                day=current_day,
                state=state,
            )
            if state["elo"] is not None:
                return True, first_seance.date_seance
            current_day += timedelta(days=1)

        return False, None

    def _cleanup_user(self, user, start_date):
        ClimberLevelDaily.objects.filter(
            user=user,
            date__gte=start_date
        ).delete()

    def _compute_user(self, user, start_date, end_date):
        for bloc in (True, False):
            self._compute_user_bloc(user, bloc, start_date, end_date)

    def _compute_user_bloc(self, user, bloc, start_date, end_date):
        state = initial_elo_state()

        previous = (
            ClimberLevelDaily.objects
            .filter(user=user, bloc=bloc, date__lt=start_date)
            .order_by("-date")
            .first()
        )

        if previous:
            state["elo"] = previous.elo
            state["ranking"] = False

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

    def _compute_trends(self, impacted):
        window_days = 7
        earliest_start = min(impacted.values())
        trend_start = earliest_start - timedelta(days=window_days)

        qs = (
            ClimberLevelDaily.objects
            .filter(
                user_id__in=impacted.keys(),
                date__gte=trend_start,
            )
            .order_by("user_id", "bloc", "date")
        )

        TrendCommand()._compute(
            qs,
            window_days=window_days,
            total_users=len(impacted),
        )
