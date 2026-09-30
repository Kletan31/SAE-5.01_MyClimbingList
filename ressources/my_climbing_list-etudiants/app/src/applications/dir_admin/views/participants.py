# applications/dir_admin/views/participants.py

from django.shortcuts import render, get_object_or_404, redirect
from applications.dir_admin.decorators.superuser_required import superuser_required
from applications.contest.models import Contest, Inscription


@superuser_required
def participants_view(request, contest_id):
    if not request.user.is_superuser:
        return redirect("dir_admin:login")

    contest = get_object_or_404(Contest, id=contest_id)
    inscriptions = Inscription.objects.filter(contest=contest).select_related("user")

    return render(request, "dir_admin/participants/participants_list.html", {
        "contest": contest,
        "inscriptions": inscriptions,
    })
