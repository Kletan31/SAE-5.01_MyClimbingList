# applications/staff_admin/views/contest_list.py

from django.shortcuts import render
from applications.contest.models import Contest
from applications.staff_admin.decorators import staff_required


@staff_required
def contest_list_view(request):
    # Salle de référence du staff
    user_salle = request.user.profile.salle_voie

    # Onglet actif (événement | permanent | passé)
    active_tab = request.GET.get("tab", "evenement")

    # Tous les contests de la salle
    contests = Contest.objects.filter(salle=user_salle)

    # --------------------------------------------------
    # Séparation permanents / non permanents
    # --------------------------------------------------
    permanents = contests.filter(is_permanent=True)
    autres = contests.filter(is_permanent=False).order_by("start_date")

    # --------------------------------------------------
    # Tri métier pour les permanents
    # --------------------------------------------------
    ordre_niveaux = {
        "Intermédiaire": 0,
        "Confirmé": 1,
        "Expert": 2,
        "Mutant": 3,
    }

    ordre_disciplines = {
        "voie": 0,
        "bloc": 1,
    }

    permanents = sorted(
        permanents,
        key=lambda c: (
            ordre_niveaux.get(c.name.split()[1], 99),
            ordre_disciplines.get(c.discipline, 99),
        )
    )

    # Ordre final (le filtrage visuel est fait côté template / JS léger)
    contests_sorted = list(permanents) + list(autres)

    return render(
        request,
        "staff_admin/contest_list/contest_list.html",
        {
            "contests": contests_sorted,
            "active_tab": active_tab,  # utile pour debug / extensions futures
        },
    )
