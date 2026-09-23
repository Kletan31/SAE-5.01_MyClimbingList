# applications/staff_admin/views/openings_stats.py

from django.shortcuts import render
from applications.staff_admin.decorators import staff_required
from django.db.models import Sum, F, Value, Q
from django.db.models.functions import Coalesce
from django.utils.timezone import localdate

from applications.core.models import Ouverture
from applications.staff_admin.utils import get_salle_from_request


@staff_required
def openings_stats_view(request, period="all"):
    """
    Page staff : statistiques d'utilisation des ouvertures (voies / blocs)

    period:
        - "all"   : toutes les séances
        - "today" : uniquement les séances du jour
    """

    # =====================================================
    # Salle du staff
    # =====================================================
    salle = get_salle_from_request(request)

    # =====================================================
    # Filtre temporel sur les séances
    # =====================================================
    seance_filter = Q()
    if period == "today":
        seance_filter = Q(seance__date_seance=localdate())

    # =====================================================
    # Ouvertures actives + agrégations
    # =====================================================
    ouvertures = (
        Ouverture.objects
        .filter(
            salle=salle,
            active=True,
        )
        .annotate(
            # ---------------------
            # Essais
            # ---------------------
            total_essais=Coalesce(
                Sum(
                    F("seance__nb_try") + F("seance__nb_try_lead"),
                    filter=seance_filter,
                ),
                Value(0),
            ),
            total_essais_lead=Coalesce(
                Sum(
                    F("seance__nb_try_lead"),
                    filter=seance_filter,
                ),
                Value(0),
            ),

            # ---------------------
            # Succès
            # ---------------------
            total_succes=Coalesce(
                Sum(
                    F("seance__nb_top") + F("seance__nb_top_lead"),
                    filter=seance_filter,
                ),
                Value(0),
            ),
            total_succes_lead=Coalesce(
                Sum(
                    F("seance__nb_top_lead"),
                    filter=seance_filter,
                ),
                Value(0),
            ),
        )
        .order_by("date_ouverture")
    )

    # =====================================================
    # Calcul des ratios + détection "today"
    # =====================================================
    openings_data = []
    has_today_openings = False

    for ouverture in ouvertures:
        essais = ouverture.total_essais
        essais_lead = ouverture.total_essais_lead

        succes = ouverture.total_succes
        succes_lead = ouverture.total_succes_lead

        ratio = succes / essais if essais > 0 else 0
        ratio_lead = succes_lead / essais_lead if essais_lead > 0 else 0

        if period == "today" and essais > 0:
            has_today_openings = True

        openings_data.append({
            "ouverture": ouverture,

            # Essais
            "total_essais": essais,
            "total_essais_lead": essais_lead,

            # Succès
            "total_succes": succes,
            "total_succes_lead": succes_lead,

            # Ratios
            "ratio": ratio,
            "ratio_lead": ratio_lead,
        })

    # =====================================================
    # Contexte template
    # =====================================================
    context = {
        "salle": salle,
        "openings": openings_data,
        "period": period,
        "has_today_openings": has_today_openings,
    }

    return render(
        request,
        "staff_admin/openings_stats/openings_stats.html",
        context
    )
