import math
from collections import defaultdict

from applications.route_event.models import (
    RouteEventParticipant,
    RouteEventPerformance,
    RouteEventRoute,
)


def get_hold_value(performance):
    if not performance or performance.hold_number <= 0:
        return 0

    return performance.hold_number + (0.5 if performance.hold_plus else 0)


def compute_ranking_points_for_route(route, participants, performances_by_participant_and_route):
    route_results = []

    for participant in participants:
        performance = performances_by_participant_and_route.get(
            (participant.id, route.id)
        )

        route_results.append(
            {
                "participant": participant,
                "hold_value": get_hold_value(performance),
                "ranking_points": None,
            }
        )

    route_results.sort(
        key=lambda row: row["hold_value"],
        reverse=True,
    )

    index = 0

    while index < len(route_results):
        current_hold_value = route_results[index]["hold_value"]

        start_index = index

        while (
            index < len(route_results)
            and route_results[index]["hold_value"] == current_hold_value
        ):
            index += 1

        end_index = index

        occupied_ranks = range(start_index + 1, end_index + 1)
        ranking_points = sum(occupied_ranks) / (end_index - start_index)

        for row in route_results[start_index:end_index]:
            row["ranking_points"] = ranking_points

    return {
        row["participant"].id: row["ranking_points"]
        for row in route_results
    }


def get_route_event_ranking(event, phase=None, gender=None):
    all_participants = (
        RouteEventParticipant.objects
        .select_related("phase")
        .filter(
            event=event,
            is_payment_validated=True,
        )
    )

    all_participants = list(all_participants)

    displayed_participants = all_participants

    if phase:
        displayed_participants = [
            participant for participant in displayed_participants
            if participant.phase_id == phase.id
        ]

    if gender:
        displayed_participants = [
            participant for participant in displayed_participants
            if participant.gender == gender
        ]

    routes = list(
        RouteEventRoute.objects
        .filter(event=event)
        .order_by("display_order", "ouverture__relais", "ouverture__id")
    )

    performances = (
        RouteEventPerformance.objects
        .filter(
            participant__in=all_participants,
            route__event=event,
        )
    )

    performances_by_participant_and_route = {
        (performance.participant_id, performance.route_id): performance
        for performance in performances
    }

    ranking_points_by_participant = defaultdict(list)
    routes_done_by_participant = defaultdict(int)

    for route in routes:
        route_ranking_points = compute_ranking_points_for_route(
            route=route,
            participants=all_participants,
            performances_by_participant_and_route=performances_by_participant_and_route,
        )

        for participant in all_participants:
            ranking_points_by_participant[participant.id].append(
                route_ranking_points[participant.id]
            )

            performance = performances_by_participant_and_route.get(
                (participant.id, route.id)
            )

            if performance and performance.hold_number > 0:
                routes_done_by_participant[participant.id] += 1

    ranking_rows = []

    for participant in displayed_participants:
        participant_ranking_points = ranking_points_by_participant.get(
            participant.id,
            [],
        )

        if participant_ranking_points:
            product = math.prod(participant_ranking_points)
            qualification_points = product ** (1 / len(participant_ranking_points))
        else:
            qualification_points = 0

        qualification_points = round(qualification_points, 3)
        routes_done = routes_done_by_participant.get(participant.id, 0)

        ranking_rows.append(
            {
                "participant": participant,
                "qualification_points": qualification_points,
                "routes_done": routes_done,
                "rank": None,
                "score_key": (
                    qualification_points,
                    -routes_done,
                ),
            }
        )

    ranking_rows.sort(key=lambda row: row["score_key"])

    previous_score_key = None
    previous_rank = None

    for index, row in enumerate(ranking_rows, start=1):
        if row["score_key"] == previous_score_key:
            row["rank"] = previous_rank
        else:
            row["rank"] = index
            previous_rank = index
            previous_score_key = row["score_key"]

    return ranking_rows