# applications/contest/views/contest_inscription.py

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from applications.contest.models import Contest, Inscription


@require_POST
@login_required
def contest_inscription_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    # Si gratuit: l'inscription est ACCEPTED d'office → vérifier le quota avant de créer
    if not contest.is_payant and not contest.can_accept(1):
        messages.error(request, "Le contest a atteint le nombre maximum de participants.")
        return redirect("contest:contest_detail", contest_id=contest.id)

    # Évite les doublons
    insc, created = Inscription.objects.get_or_create(
        contest=contest,
        user=request.user,
        defaults={
            "status": (
                Inscription.Status.ACCEPTED
                if not contest.is_payant
                else Inscription.Status.PENDING
            )
        },
    )

    # Option: si déjà inscrit et gratuit mais quota vient d'être plein, on ne change rien.
    # (si tu veux gérer une 're-demande' après un refus, on pourra ajouter une route dédiée)

    return redirect("contest:contest_detail", contest_id=contest.id)
