# applications/staff_admin/views/edit_contest.py

from django.shortcuts import get_object_or_404, render, redirect

from applications.contest.models import Contest, ContestResult, Inscription
from applications.staff_admin.forms import ContestForm
from applications.staff_admin.decorators import staff_required


@staff_required
def edit_contest_view(request, pk):
    contest = get_object_or_404(
        Contest,
        pk=pk,
        created_by=request.user,
    )

    # On garde une référence à l'ancien contest de départ
    old_initial_contest = contest.initial_contest

    if request.method == "POST":
        post_data = request.POST.copy()

        # ------------------------------------
        # NORMALISATION DES OUVERTURES (clé)
        # ------------------------------------
        ouvertures_raw = post_data.getlist("ouvertures")

        if len(ouvertures_raw) == 1 and "," in ouvertures_raw[0]:
            ids = [
                oid.strip()
                for oid in ouvertures_raw[0].split(",")
                if oid.strip()
            ]
            post_data.setlist("ouvertures", ids)

        form = ContestForm(
            post_data,
            instance=contest,
            user=request.user,
        )

        if form.is_valid():
            contest = form.save(commit=False)

            # Détection changement de contest de départ
            initial_contest_changed = (
                old_initial_contest != contest.initial_contest
            )

            contest.save()
            form.save_m2m()

            # Mise à jour discipline / combiné
            contest.update_discipline_from_ouvertures()
            contest.save(update_fields=["discipline", "is_combine"])

            # ------------------------------------
            # INVALIDATION DES score_initial
            # ------------------------------------
            if initial_contest_changed:
                Inscription.objects.filter(
                    contest=contest
                ).update(score_initial=None)

            # ------------------------------------
            # Nettoyage des ContestResult incohérents
            # ------------------------------------
            current_ouverture_ids = set(
                contest.ouvertures.values_list("id", flat=True)
            )

            ContestResult.objects.filter(
                contest=contest
            ).exclude(
                ouverture_id__in=current_ouverture_ids
            ).delete()

            return redirect("staff_admin:contest_list")

    else:
        form = ContestForm(
            instance=contest,
            user=request.user,
        )

    return render(
        request,
        "staff_admin/edit_contest/edit_contest.html",
        {
            "form": form,
            "contest": contest,
        },
    )
