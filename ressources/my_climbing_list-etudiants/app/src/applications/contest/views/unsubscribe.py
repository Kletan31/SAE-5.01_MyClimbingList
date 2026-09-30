# applications/contest/views/unsubscribe.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from applications.contest.models import Contest, Inscription


@login_required
def unsubscribe_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    # Supprime l'inscription de l'utilisateur connecté
    Inscription.objects.filter(contest=contest, user=request.user).delete()

    # Redirige vers la page de la salle concernée
    return redirect("contest:salle_detail", contest.salle.id)
