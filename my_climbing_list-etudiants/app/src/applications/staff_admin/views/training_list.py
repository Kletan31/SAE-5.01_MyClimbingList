# applications/staff_admin/views/training_list.py

from applications.staff_admin.decorators import staff_required
from django.shortcuts import render

from applications.custom_auth.models import Profile
from applications.staff_admin.utils import get_salle_from_request


@staff_required
def training_list_view(request):
    """
    Liste des grimpeurs ayant autorisé la salle du staff
    à consulter leurs séances (suivi d'entraînement).
    """

    # Salle du staff (ta source de vérité existante)
    salle = get_salle_from_request(request)

    if not salle:
        return render(
            request,
            "staff_admin/training/training_list.html",
            {
                "error": "Aucune salle associée à ce compte staff.",
            },
        )

    # Profils ayant autorisé CETTE salle
    profiles = (
        Profile.objects
        .filter(authorized_salles=salle)
        .select_related("user")
        .order_by("user__username")
    )

    context = {
        "salle": salle,
        "profiles": profiles,
    }

    return render(
        request,
        "staff_admin/training/training_list.html",
        context,
    )
