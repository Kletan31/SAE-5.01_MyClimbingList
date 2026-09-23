from datetime import datetime

from django.utils import timezone


def is_team_phase_open(team):
    event_date = team.event.date
    phase = team.phase

    start_datetime = datetime.combine(event_date, phase.start_time)
    end_datetime = datetime.combine(event_date, phase.end_time)

    start_datetime = timezone.make_aware(start_datetime)
    end_datetime = timezone.make_aware(end_datetime)

    now = timezone.now()

    return start_datetime <= now <= end_datetime