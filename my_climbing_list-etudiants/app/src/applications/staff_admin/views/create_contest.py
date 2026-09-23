# applications/staff_admin/views/create_contest.py

from django.shortcuts import render, redirect
from applications.staff_admin.forms import ContestForm
from applications.staff_admin.decorators import staff_required


@staff_required
def create_contest_view(request):
    if request.method == "POST":
        post_data = request.POST.copy()

        ouvertures_ids = post_data.get("ouvertures", "")
        if ouvertures_ids:
            id_list = [pk.strip() for pk in ouvertures_ids.split(",") if pk.strip()]
            post_data.setlist("ouvertures", id_list)

        form = ContestForm(post_data, user=request.user)

        if form.is_valid():
            contest = form.save(commit=False)
            contest.salle = request.user.profile.salle_voie  # type: ignore
            contest.created_by = request.user
            contest.save()
            form.save_m2m()

            contest.update_discipline_from_ouvertures()
            contest.save(update_fields=["discipline", "is_combine"])

            return redirect("staff_admin:dashboard")

    else:
        form = ContestForm(user=request.user)

    return render(
        request,
        "staff_admin/create_contest/create_contest.html",
        {"form": form},
    )
