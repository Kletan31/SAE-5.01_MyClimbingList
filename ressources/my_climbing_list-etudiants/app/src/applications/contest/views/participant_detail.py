# applications/contest/views/participant_detail.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from applications.contest.models import Contest
from applications.contest.utils.participant_detail_core import participant_detail_core


@login_required
def participant_detail_view(request, contest_id, user_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    user = get_object_or_404(User, pk=user_id)

    return participant_detail_core(
        request=request,
        contest=contest,
        membres=[user],
        participant=user,
        is_team=False,
    )
