from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from applications.contest.models import Contest, Team
from applications.contest.utils.participant_detail_core import participant_detail_core


@login_required
def team_detail_view(request, contest_id, team_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    team = get_object_or_404(Team, pk=team_id, contest=contest)

    return participant_detail_core(
        request=request,
        contest=contest,
        membres=team.members.all(),
        participant=team,
        is_team=True,
    )
