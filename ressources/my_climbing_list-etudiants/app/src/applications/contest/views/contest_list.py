# applications/contest/views/contest_list.py

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from applications.custom_auth.models import Salle
from applications.contest.models import Contest


@login_required
def salle_contest_list_view(request, salle_id):
    salle = get_object_or_404(Salle, pk=salle_id)

    base_qs = Contest.objects.filter(
        salle=salle,
        is_active=True,
    )

    # =====================================================
    # 1. CONTESTS PERMANENTS (activés)
    # =====================================================
    permanents_qs = base_qs.filter(
        is_permanent=True,
        is_permanent_enabled=True,
    )

    niveau_order = {
        "Intermédiaire": 0,
        "Confirmé": 1,
        "Expert": 2,
        "Mutant": 3,
    }

    def permanent_sort_key(contest):
        # --- Niveau ---
        niveau = 99
        for key, value in niveau_order.items():
            if key in contest.name:
                niveau = value
                break

        # --- Discipline : Voie avant Bloc ---
        discipline = 0 if contest.discipline == Contest.VOIE else 1

        return niveau, discipline

    permanents = sorted(permanents_qs, key=permanent_sort_key)

    # =====================================================
    # 2. CONTESTS NON PERMANENTS
    # =====================================================
    non_permanents = (
        base_qs
        .filter(is_permanent=False)
        .order_by("-start_date")
    )

    # =====================================================
    # 3. ORDRE FINAL
    # =====================================================
    contests = list(permanents) + list(non_permanents)

    return render(
        request,
        "contest/contest_list/contest_list.html",
        {
            "salle": salle,
            "contests": contests,
            "now": now(),
        }
    )
