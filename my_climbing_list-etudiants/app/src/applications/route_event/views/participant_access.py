from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from applications.route_event.models import (
    RouteEventParticipant,
    RouteEventPerformance,
    RouteEventRoute,
)
from applications.route_event.utils import is_participant_phase_open


def participant_access(request, token):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related(
            "event",
            "phase",
        ),
        access_token=token,
    )

    event = participant.event

    if not participant.is_payment_validated:
        return render(
            request,
            "route_event/participant_access.html",
            {
                "participant": participant,
                "event": event,
                "is_waiting_validation": True,
            },
        )

    routes = (
        RouteEventRoute.objects
        .select_related("ouverture")
        .filter(event=event)
        .order_by("display_order", "ouverture__relais", "ouverture__id")
    )

    is_phase_open = is_participant_phase_open(participant)

    if request.method == "POST":
        if not is_phase_open:
            return HttpResponseForbidden(
                "La phase de saisie est fermée. Les résultats ne peuvent plus être modifiés."
            )

        for route in routes:
            hold_number_key = f"route_{route.id}_hold_number"
            hold_plus_key = f"route_{route.id}_hold_plus"

            raw_hold_number = request.POST.get(hold_number_key, "0").strip()
            hold_plus = hold_plus_key in request.POST

            try:
                hold_number = int(raw_hold_number) if raw_hold_number else 0
            except ValueError:
                hold_number = 0

            if hold_number < 0:
                hold_number = 0

            if hold_number == 0:
                hold_plus = False

            RouteEventPerformance.objects.update_or_create(
                participant=participant,
                route=route,
                defaults={
                    "hold_number": hold_number,
                    "hold_plus": hold_plus,
                },
            )

        messages.success(request, "Vos résultats ont bien été enregistrés.")

        return redirect(
            "route_event:participant_access",
            token=participant.access_token,
        )

    performances = RouteEventPerformance.objects.filter(
        participant=participant,
        route__in=routes,
    )

    performance_by_route = {
        performance.route_id: performance
        for performance in performances
    }

    route_rows = []

    for route in routes:
        route_rows.append(
            {
                "route": route,
                "performance": performance_by_route.get(route.id),
            }
        )

    return render(
        request,
        "route_event/participant_access.html",
        {
            "participant": participant,
            "event": event,
            "is_waiting_validation": False,
            "is_phase_open": is_phase_open,
            "route_rows": route_rows,
        },
    )