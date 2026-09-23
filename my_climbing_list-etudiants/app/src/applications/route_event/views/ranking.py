from django.shortcuts import get_object_or_404, render

from applications.route_event.decorators import (
    route_event_staff_required,
)
from applications.route_event.models import (
    RouteEvent,
    RouteEventPhase,
    RouteEventParticipant,
)
from applications.route_event.permissions import (
    get_staff_event_or_404,
)
from applications.route_event.services.ranking import (
    get_route_event_ranking,
)
from applications.route_event.services.route_rankings import (
    get_route_rankings,
)
from applications.route_event.services.export import (
    build_ranking_csv_response,
    build_ranking_pdf_response,
)


def participant_ranking(request, token):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related(
            "event",
            "phase",
        ),
        access_token=token,
    )

    if not participant.is_payment_validated:
        return render(
            request,
            "route_event/participant_access.html",
            {
                "participant": participant,
                "event": participant.event,
                "is_waiting_validation": True,
            },
        )

    event = participant.event

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            RouteEventPhase,
            id=phase_id,
            event=event,
        )

    selected_gender = request.GET.get("gender")

    if selected_gender not in ["M", "F"]:
        selected_gender = None

    ranking_rows = get_route_event_ranking(
        event=event,
        phase=selected_phase,
        gender=selected_gender,
    )

    phases = event.phases.all().order_by(
        "start_time"
    )

    return render(
        request,
        "route_event/ranking.html",
        {
            "event": event,
            "participant": participant,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "selected_gender": selected_gender,
            "is_staff_view": False,
            "is_public_view": False,
        },
    )


def public_ranking(request, slug):
    event = get_object_or_404(
        RouteEvent,
        slug=slug,
    )

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            RouteEventPhase,
            id=phase_id,
            event=event,
        )

    selected_gender = request.GET.get("gender")

    if selected_gender not in ["M", "F"]:
        selected_gender = None

    ranking_rows = get_route_event_ranking(
        event=event,
        phase=selected_phase,
        gender=selected_gender,
    )

    phases = event.phases.all().order_by(
        "start_time"
    )

    return render(
        request,
        "route_event/ranking.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "selected_gender": selected_gender,
            "is_staff_view": False,
            "is_public_view": True,
        },
    )


@route_event_staff_required
def staff_ranking(request, slug):
    event = get_staff_event_or_404(
        request,
        slug,
    )

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            RouteEventPhase,
            id=phase_id,
            event=event,
        )

    selected_gender = request.GET.get("gender")

    if selected_gender not in ["M", "F"]:
        selected_gender = None

    ranking_rows = get_route_event_ranking(
        event=event,
        phase=selected_phase,
        gender=selected_gender,
    )

    phases = event.phases.all().order_by(
        "start_time"
    )

    return render(
        request,
        "route_event/ranking.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
            "selected_gender": selected_gender,
            "is_staff_view": True,
            "is_public_view": False,
        },
    )


@route_event_staff_required
def staff_ranking_display(request, slug):
    event = get_staff_event_or_404(
        request,
        slug,
    )

    phase_id = request.GET.get("phase")
    selected_phase = None

    if phase_id:
        selected_phase = get_object_or_404(
            RouteEventPhase,
            id=phase_id,
            event=event,
        )

    ranking_rows = get_route_event_ranking(
        event=event,
        phase=selected_phase,
    )

    phases = event.phases.all().order_by(
        "start_time"
    )

    return render(
        request,
        "route_event/staff/ranking_display.html",
        {
            "event": event,
            "ranking_rows": ranking_rows,
            "phases": phases,
            "selected_phase": selected_phase,
        },
    )


def participant_route_rankings(request, token):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related(
            "event",
            "phase",
        ),
        access_token=token,
    )

    if not participant.is_payment_validated:
        return render(
            request,
            "route_event/participant_access.html",
            {
                "participant": participant,
                "event": participant.event,
                "is_waiting_validation": True,
            },
        )

    event = participant.event

    route_sections = get_route_rankings(
        event,
    )

    return render(
        request,
        "route_event/route_rankings.html",
        {
            "event": event,
            "participant": participant,
            "route_sections": route_sections,
            "is_public_view": False,
        },
    )


def public_route_rankings(request, slug):
    event = get_object_or_404(
        RouteEvent,
        slug=slug,
    )

    route_sections = get_route_rankings(
        event,
    )

    return render(
        request,
        "route_event/route_rankings.html",
        {
            "event": event,
            "route_sections": route_sections,
            "is_public_view": True,
        },
    )


@route_event_staff_required
def staff_route_rankings(request, slug):
    event = get_staff_event_or_404(
        request,
        slug,
    )

    route_sections = get_route_rankings(
        event,
    )

    return render(
        request,
        "route_event/route_rankings.html",
        {
            "event": event,
            "route_sections": route_sections,
            "is_public_view": False,
            "is_staff_view": True,
        },
    )

@route_event_staff_required
def staff_ranking_export_csv(request, slug):
    event = get_staff_event_or_404(
        request,
        slug,
    )

    return build_ranking_csv_response(event)


@route_event_staff_required
def staff_ranking_export_pdf(request, slug):
    event = get_staff_event_or_404(
        request,
        slug,
    )

    return build_ranking_pdf_response(event)