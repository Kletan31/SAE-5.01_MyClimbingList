# applications/staff_admin/views/# applications/staff_admin/views/auth.py

from django.shortcuts import render, get_object_or_404, redirect
from applications.contest.models import Contest
from applications.staff_admin.decorators import staff_required


@staff_required
def delete_contest_view(request, pk):
    contest = get_object_or_404(Contest, pk=pk, created_by=request.user)

    if request.method == "POST":
        contest.delete()
        return redirect("staff_admin:contest_list")

    return render(request, "staff_admin/delete_contest/delete_contest.html", {"contest": contest})
