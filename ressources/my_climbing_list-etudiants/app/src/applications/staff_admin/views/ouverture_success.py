# applications/staff_admin/views/ouverture_success.py

from django.shortcuts import render, get_object_or_404
from applications.core.models import Seance
from applications.contest.models import Contest, Inscription, ContestResult
from applications.staff_admin.decorators import staff_required


# noinspection PyUnresolvedReferences
@staff_required
def ouverture_success_view(request, contest_id, ouverture_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    ouverture = get_object_or_404(contest.ouvertures, pk=ouverture_id)

    # Participants "actifs" selon le type de contest
    if contest.is_payant:
        inscriptions_qs = Inscription.objects.filter(
            contest=contest, status=Inscription.Status.ACCEPTED
        )
    else:
        inscriptions_qs = Inscription.objects.filter(contest=contest).exclude(
            status=Inscription.Status.REFUSED
        )

    inscriptions = inscriptions_qs.values_list("user_id", flat=True)

    # 🛠 Récupérer la liste des relais en tête pour la salle de l'ouverture
    relais_en_tete = ouverture.salle.relais_en_tete if ouverture.salle else []

    # Condition : est-ce grimpable en tête ?
    grimpable_en_tete = (not ouverture.bloc) and (ouverture.relais in relais_en_tete)

    if contest.is_permanent:
        seances = (
            Seance.objects
            .filter(
                ouverture=ouverture,
                user_id__in=inscriptions,
            )
            .select_related("user")
        )
        user_ids = {s.user_id for s in seances}
    else:
        seances = (
            ContestResult.objects
            .filter(
                contest=contest,
                ouverture=ouverture,
                user_id__in=inscriptions
            )
            .select_related("user")
        )
        # On ne compte que ceux qui ont topé dans le cadre événementiel
        user_ids = {r.user_id for r in seances if r.has_top}

    user_count = len(user_ids)

    return render(request, "staff_admin/ouverture_success/ouverture_success.html", {
        "ouverture": ouverture,
        "contest": contest,
        "seances": seances,
        "user_count": user_count,
        "grimpable_en_tete": grimpable_en_tete,
    })
