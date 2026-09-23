from applications.event.models import EventPerformance, EventTeam


def get_event_ranking(event, phase=None):
    teams = (
        EventTeam.objects
        .select_related("participant_1", "participant_2", "phase")
        .filter(event=event, is_payment_validated=True)
    )

    if phase:
        teams = teams.filter(phase=phase)

    teams = list(teams)

    participant_ids = []
    for team in teams:
        participant_ids.append(team.participant_1_id)
        participant_ids.append(team.participant_2_id)

    performances = (
        EventPerformance.objects
        .select_related("route")
        .filter(
            participant_id__in=participant_ids,
            route__event=event,
        )
    )

    scores_by_participant = {}

    for performance in performances:
        participant_score = scores_by_participant.setdefault(
            performance.participant_id,
            {
                "points": 0,
                "tops": 0,
                "zones": 0,
            },
        )

        if performance.top:
            participant_score["points"] += performance.route.points
            participant_score["tops"] += 1

        if performance.zone:
            participant_score["zones"] += 1

    ranking_rows = []

    for team in teams:
        p1_score = scores_by_participant.get(
            team.participant_1_id,
            {"points": 0, "tops": 0, "zones": 0},
        )

        p2_score = scores_by_participant.get(
            team.participant_2_id,
            {"points": 0, "tops": 0, "zones": 0},
        )

        points = p1_score["points"] + p2_score["points"]
        tops = p1_score["tops"] + p2_score["tops"]
        zones = p1_score["zones"] + p2_score["zones"]

        ranking_rows.append(
            {
                "team": team,
                "points": points,
                "tops": tops,
                "zones": zones,
                "score_key": (points, tops, zones),
                "rank": None,
                "is_mixed_qualified": False,
            }
        )

    ranking_rows.sort(
        key=lambda row: (
            row["points"],
            row["tops"],
            row["zones"],
        ),
        reverse=True,
    )

    previous_score_key = None
    previous_rank = None

    for index, row in enumerate(ranking_rows, start=1):
        if row["score_key"] == previous_score_key:
            row["rank"] = previous_rank
        else:
            row["rank"] = index
            previous_rank = index
            previous_score_key = row["score_key"]

    mixed_rows = [
        row for row in ranking_rows
        if row["team"].team_type == EventTeam.TEAM_TYPE_MIXED
    ]

    for row in mixed_rows[:6]:
        row["is_mixed_qualified"] = True

    return ranking_rows