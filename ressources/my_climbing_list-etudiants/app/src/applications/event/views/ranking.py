from django.shortcuts import get_object_or_404, render

from applications.event.decorators import event_staff_required
from applications.event.models import Event, EventPhase, EventTeam
from applications.event.permissions import get_staff_event_or_404
from applications.event.services.ranking import get_event_ranking


def get_filtered_ranking_rows(request, event, selected_phase):
    show_only_finalists = (
        request.GET.get("finalists") == "1"
        and selected_phase is None
    )

    ranking_rows = get_event_ranking(
        event=event,
        phase=selected_phase,
    )

    if show_only_finalists:
        ranking_rows = [
            row for row in ranking_rows
            if row["is_mixed_qualified"]
        ]

    return ranking_rows, show_only_finalists


def team_ranking(request, token):
    team = get_object_or_404(
        EventTeam.objects.select_related("event"),
        access_token=token,
    )

    if not team.is_payment_validated:
        return render(
            request,
            "event/team_access.html",
            {
                "team": team,
                "event": team.event,
                "is_waiting_validation": True,
            },
        )

    event = team.event
    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            EventPhase,
            id=phase_id,
            event=event,
        )

    ranking_rows, show_only_finalists = get_filtered_ranking_rows(
        request=request,
        event=event,
        selected_phase=selected_phase,
    )

    phases = event.phases.all().order_by("start_time")

    return render(
        request,
        "event/ranking.html",
        {
            "event": event,
            "team": team,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "is_staff_view": False,
            "show_finalist_badge": selected_phase is None,
            "show_only_finalists": show_only_finalists,
        },
    )


@event_staff_required
def staff_ranking(request, slug):
    event = get_staff_event_or_404(request, slug)

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            EventPhase,
            id=phase_id,
            event=event,
        )

    ranking_rows, show_only_finalists = get_filtered_ranking_rows(
        request=request,
        event=event,
        selected_phase=selected_phase,
    )

    phases = event.phases.all().order_by("start_time")

    return render(
        request,
        "event/ranking.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "is_staff_view": True,
            "show_finalist_badge": selected_phase is None,
            "show_only_finalists": show_only_finalists,
        },
    )


@event_staff_required
def staff_ranking_display(request, slug):
    event = get_staff_event_or_404(request, slug)

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            EventPhase,
            id=phase_id,
            event=event,
        )

    ranking_rows, show_only_finalists = get_filtered_ranking_rows(
        request=request,
        event=event,
        selected_phase=selected_phase,
    )

    phases = event.phases.all().order_by("start_time")

    return render(
        request,
        "event/staff/ranking_display.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "show_finalist_badge": selected_phase is None,
            "show_only_finalists": show_only_finalists,
        },
    )


def public_ranking(request, slug):
    event = get_object_or_404(
        Event,
        slug=slug,
    )

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            EventPhase,
            id=phase_id,
            event=event,
        )

    ranking_rows, show_only_finalists = get_filtered_ranking_rows(
        request=request,
        event=event,
        selected_phase=selected_phase,
    )

    phases = event.phases.all().order_by("start_time")

    return render(
        request,
        "event/ranking.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "is_staff_view": False,
            "is_public_view": True,
            "show_finalist_badge": selected_phase is None,
            "show_only_finalists": show_only_finalists,
        },
    )