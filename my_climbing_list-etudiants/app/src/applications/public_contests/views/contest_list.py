# applications/public_contests/views/contest_list.py

from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils.timezone import now

from applications.contest.models import Contest


def contest_list_view(request):
    now_ = now()
    grace_period = timedelta(days=1)
    visible_until = now_ - grace_period  # contests terminés visibles encore 24h

    # Base queryset : contests visibles
    contests = (
        Contest.objects
        .filter(
            is_active=True,
            is_permanent=False,
            start_date__lte=now_,
        )
        .filter(
            Q(end_date__isnull=True) | Q(end_date__gte=visible_until)
        )
        .select_related("salle")
        .order_by("end_date", "start_date")
    )

    # Séparation logique (au bon endroit : la vue)
    contests_en_cours = [
        contest
        for contest in contests
        if contest.end_date is None or contest.end_date >= now_
    ]

    contests_termines = [
        contest
        for contest in contests
        if contest.end_date is not None and contest.end_date < now_
    ]

    return render(
        request,
        "public_contests/contest_list/contest_list.html",
        {
            "contests_en_cours": contests_en_cours,
            "contests_termines": contests_termines,
        },
    )
