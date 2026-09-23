# applications/staff_admin/views/opening_climbers.py

from django.shortcuts import render, get_object_or_404
from applications.staff_admin.decorators import staff_required
from django.db.models import Sum, Max, F, Value
from django.db.models.functions import Coalesce
from django.utils.timezone import localdate

from applications.core.models import Ouverture, Seance
from applications.staff_admin.utils import get_salle_from_request


@staff_required
def opening_climbers_view(request, ouverture_id, period=None):
    """
    Page staff : liste des grimpeurs ayant essayé une ouverture donnée
    - global : toutes les séances
    - today  : uniquement les séances du jour
    """

    # =====================================================
    # Salle du staff
    # =====================================================
    salle = get_salle_from_request(request)

    # =====================================================
    # Ouverture (sécurisée par salle)
    # =====================================================
    ouverture = get_object_or_404(
        Ouverture,
        id=ouverture_id,
        salle=salle,
        active=True,
    )

    # =====================================================
    # Base queryset des séances
    # =====================================================
    seances = Seance.objects.filter(ouverture=ouverture)

    # =====================================================
    # Filtre "Aujourd'hui"
    # =====================================================
    if period == "today":
        seances = seances.filter(date_seance=localdate())

    # =====================================================
    # Agrégation par grimpeur
    # =====================================================
    climbers = (
        seances
        .values("user__id", "user__username")
        .annotate(
            # Essais
            total_essais=Coalesce(
                Sum(F("nb_try") + F("nb_try_lead")),
                Value(0),
            ),
            total_essais_lead=Coalesce(
                Sum(F("nb_try_lead")),
                Value(0),
            ),

            # Succès
            total_succes=Coalesce(
                Sum(F("nb_top") + F("nb_top_lead")),
                Value(0),
            ),
            total_succes_lead=Coalesce(
                Sum(F("nb_top_lead")),
                Value(0),
            ),

            # Dernier passage
            last_try=Max("date_seance"),
        )
        .order_by("user__username")
    )

    # =====================================================
    # Contexte template
    # =====================================================
    context = {
        "ouverture": ouverture,
        "climbers": climbers,
        "period": period,
    }

    return render(
        request,
        "staff_admin/openings_stats/opening_climbers.html",
        context
    )
