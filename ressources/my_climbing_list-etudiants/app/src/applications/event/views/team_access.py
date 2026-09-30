from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from applications.event.models import EventPerformance, EventRoute, EventTeam
from applications.event.utils import is_team_phase_open


def team_access(request, token):
    team = get_object_or_404(
        EventTeam.objects.select_related(
            "event",
            "phase",
            "participant_1",
            "participant_2",
        ),
        access_token=token,
    )

    event = team.event
    participants = [team.participant_1, team.participant_2]

    if not team.is_payment_validated:
        return render(
            request,
            "event/team_access.html",
            {
                "team": team,
                "event": event,
                "is_waiting_validation": True,
            },
        )

    routes = (
        EventRoute.objects.select_related("ouverture")
        .filter(event=event)
        .order_by("display_order", "ouverture__relais", "ouverture__id")
    )

    is_phase_open = is_team_phase_open(team)

    if request.method == "POST":
        if not is_phase_open:
            return HttpResponseForbidden(
                "La phase de saisie est fermée. Les résultats ne peuvent plus être modifiés."
            )

        for route in routes:
            for participant in participants:
                top_key = f"participant_{participant.id}_route_{route.id}_top"
                zone_key = f"participant_{participant.id}_route_{route.id}_zone"

                top = top_key in request.POST
                zone = zone_key in request.POST

                if top and route.has_zone:
                    zone = True

                if not route.has_zone:
                    zone = False

                EventPerformance.objects.update_or_create(
                    participant=participant,
                    route=route,
                    defaults={
                        "top": top,
                        "zone": zone,
                    },
                )

        messages.success(request, "Les résultats ont bien été enregistrés.")
        return redirect("event:team_access", token=team.access_token)

    performances = EventPerformance.objects.filter(
        participant__in=participants,
        route__in=routes,
    )

    performance_by_participant_and_route = {
        (performance.participant_id, performance.route_id): performance
        for performance in performances
    }

    route_rows = []

    for route in routes:
        route_rows.append(
            {
                "route": route,
                "participant_1_performance": performance_by_participant_and_route.get(
                    (team.participant_1_id, route.id)
                ),
                "participant_2_performance": performance_by_participant_and_route.get(
                    (team.participant_2_id, route.id)
                ),
            }
        )

    return render(
        request,
        "event/team_access.html",
        {
            "team": team,
            "event": event,
            "is_waiting_validation": False,
            "is_phase_open": is_phase_open,
            "route_rows": route_rows,
        },
    )