# applications/staff_admin/views/inscriptions.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from applications.staff_admin.decorators import staff_required
from applications.contest.models import Contest, Inscription


STATUS_ALIAS = {
    # compat anciens paramètres
    "valid": Inscription.Status.ACCEPTED,
    "pending": Inscription.Status.PENDING,
    # nouveaux paramètres explicites
    "accepted": Inscription.Status.ACCEPTED,
    "refused": Inscription.Status.REFUSED,
    "en_attente": Inscription.Status.PENDING,  # alias FR si besoin
}


@staff_required
def inscriptions_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    # --- Filtres ---
    status_filter_key = request.GET.get("status")
    status_choice = STATUS_ALIAS.get(status_filter_key) if status_filter_key else None

    qs = (Inscription.objects
          .filter(contest=contest)
          .select_related("user")
          .order_by("-date_inscription"))

    if status_choice:
        qs = qs.filter(status=status_choice)

    # --- Actions POST (valider / refuser / remettre en attente) ---
    if request.method == "POST":
        inscription_id = request.POST.get("inscription_id")
        action = request.POST.get("action")  # "accept" | "refuse" | "pending"

        insc = get_object_or_404(Inscription, id=inscription_id, contest=contest)

        if action == "accept":
            # quota : uniquement si on change vers ACCEPTED
            if insc.status != Inscription.Status.ACCEPTED and not contest.can_accept(1):
                messages.error(request, "Le contest a atteint le nombre maximum de participants.")
            else:
                insc.status = Inscription.Status.ACCEPTED
                insc.save(update_fields=["status"])
                messages.success(request, f"Inscription validée pour {insc.user}.")
        elif action == "refuse":
            insc.status = Inscription.Status.REFUSED
            insc.save(update_fields=["status"])
            messages.success(request, f"Inscription refusée pour {insc.user}.")
        elif action == "pending":
            insc.status = Inscription.Status.PENDING
            insc.save(update_fields=["status"])
            messages.success(request, f"Inscription remise en attente pour {insc.user}.")
        else:
            messages.error(request, "Action invalide.")

        # conserver le filtre courant dans l’URL après action
        url = reverse("staff_admin:inscriptions", kwargs={"contest_id": contest.id})
        if status_filter_key:
            url = f"{url}?status={status_filter_key}"
        return redirect(url)

    # --- Compteurs pour l’UI ---
    counts = {
        "accepted": contest.inscriptions.filter(status=Inscription.Status.ACCEPTED).count(),
        "pending": contest.inscriptions.filter(status=Inscription.Status.PENDING).count(),
        "refused": contest.inscriptions.filter(status=Inscription.Status.REFUSED).count(),
        "total": contest.inscriptions.count(),
    }

    context = {
        "contest": contest,
        "inscriptions": qs,
        "status_filter": status_filter_key,
        "counts": counts,
        "is_unlimited": contest.is_unlimited,
        "is_full": contest.is_full,
        "remaining_slots": contest.remaining_slots,
        "max_participants": contest.max_participants,
    }
    return render(request, "staff_admin/inscriptions/inscriptions.html", context)
