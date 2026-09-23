# applications/contest/views/contest_detail.py

from django.shortcuts import render, redirect
from applications.contest.models import Contest, Inscription
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now


@login_required
def contest_detail_view(request, contest_id):
    try:
        contest = Contest.objects.get(pk=contest_id)
    except Contest.DoesNotExist:
        referer = request.META.get("HTTP_REFERER")
        redirect_url = referer if referer else reverse("core:home")
        return render(request, "contest/utils/clear_contest_cache.html", {
            "redirect_url": redirect_url,
        })

    # --- État temporel
    now_ = now()
    has_started = contest.start_date <= now_
    has_ended = bool(contest.end_date and contest.end_date < now_)
    is_running = contest.is_running  # garde la logique existante (is_active & fenêtre temporelle)

    # 🎯 Si non-permanent ET terminé → classement
    if not contest.is_permanent and has_ended:
        return redirect("contest:classement_topo", contest_id=contest.id)

    # Inscription de l'utilisateur
    inscription = Inscription.objects.filter(contest=contest, user=request.user).first()
    is_registered = bool(inscription)

    # Règle d'accès (ne servira pour la redirection qu'en cours)
    can_access = False
    status = None
    if is_registered:
        status = inscription.status
        if contest.is_payant:
            can_access = (status == Inscription.Status.ACCEPTED)
        else:
            can_access = (status != Inscription.Status.REFUSED)

    # ✅ Rediriger vers topo/classement uniquement si le contest est EN COURS
    if is_running and is_registered and can_access:
        return redirect("contest:classement_topo", contest_id=contest.id)

    return render(request, "contest/contest_detail/contest_detail.html", {
        "contest": contest,
        "is_registered": is_registered,
        "status": status,         # pour les messages dans le template
        "can_access": can_access,  # utile si tu veux indiquer “accès dès le début”
        "has_started": has_started,
        "has_ended": has_ended,
        "is_running": is_running,
    })
