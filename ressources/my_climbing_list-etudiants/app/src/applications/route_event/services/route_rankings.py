from applications.route_event.models import (
    RouteEventParticipant,
    RouteEventPerformance,
    RouteEventRoute,
)
from applications.route_event.services.ranking import get_hold_value


def get_route_rankings(event):
    participants = list(
        RouteEventParticipant.objects
        .select_related("phase")
        .filter(
            event=event,
            is_payment_validated=True,
        )
        .order_by("last_name", "first_name")
    )

    routes = list(
        RouteEventRoute.objects
        .select_related("ouverture")
        .filter(event=event)
        .order_by("display_order", "ouverture__relais", "ouverture__id")
    )

    performances = RouteEventPerformance.objects.filter(
        participant__in=participants,
        route__in=routes,
    )

    performances_by_participant_and_route = {
        (performance.participant_id, performance.route_id): performance
        for performance in performances
    }

    route_sections = []

    for route in routes:
        rows = []

        for participant in participants:
            performance = performances_by_participant_and_route.get(
                (participant.id, route.id)
            )

            rows.append(
                {
                    "participant": participant,
                    "performance": performance,
                    "hold_value": get_hold_value(performance),
                    "rank": None,
                    "ranking_points": None,
                }
            )

        rows.sort(
            key=lambda row: row["hold_value"],
            reverse=True,
        )

        index = 0

        while index < len(rows):
            current_hold_value = rows[index]["hold_value"]
            start_index = index

            while (
                index < len(rows)
                and rows[index]["hold_value"] == current_hold_value
            ):
                index += 1

            end_index = index
            occupied_ranks = range(start_index + 1, end_index + 1)
            ranking_points = sum(occupied_ranks) / (end_index - start_index)
            rank = start_index + 1

            for row in rows[start_index:end_index]:
                row["rank"] = rank
                row["ranking_points"] = round(ranking_points, 3)

        route_sections.append(
            {
                "route": route,
                "rows": rows,
            }
        )

    return route_sections