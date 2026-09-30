# applications/staff_admin/views/training_calendar.py

from calendar import monthrange
from datetime import date
from collections import defaultdict

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localdate
from django.utils.formats import date_format
from django.utils.translation import gettext as gettext
from django.contrib.auth import get_user_model

from applications.core.models import Seance

User = get_user_model()


def staff_required(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(staff_required)
def training_calendar_view(request, user_id):
    """
    Calendrier mensuel du suivi d'entraînement d'un grimpeur
    + détail des séances du jour sélectionné
    (groupées par salle, puis par discipline)
    """

    climber = get_object_or_404(User, id=user_id)

    # --------------------------------------------------
    # Date de référence
    # --------------------------------------------------
    today = localdate()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    day = request.GET.get("day")

    selected_day = int(day) if day and day.isdigit() else None
    selected_date = (
        date(year, month, selected_day)
        if selected_day and 1 <= selected_day <= monthrange(year, month)[1]
        else None
    )

    # --------------------------------------------------
    # Infos mois
    # --------------------------------------------------
    first_day = date(year, month, 1)
    days_in_month = monthrange(year, month)[1]
    month_label = date_format(first_day, "F")

    # --------------------------------------------------
    # Séances du mois
    # --------------------------------------------------
    seances_month = (
        Seance.objects
        .filter(
            user=climber,
            date_seance__year=year,
            date_seance__month=month,
        )
        .select_related("ouverture", "ouverture__salle")
        .order_by("date_seance")
    )

    days_with_seance = {s.date_seance.day for s in seances_month}

    # --------------------------------------------------
    # Séances du jour sélectionné (GROUPÉES PAR SALLE)
    # --------------------------------------------------
    salles_data = []

    if selected_date:
        # structure temporaire
        salles_map = defaultdict(lambda: {"voie": [], "bloc": []})

        for s in seances_month:
            if s.date_seance != selected_date:
                continue

            ouverture = s.ouverture
            salle = ouverture.salle
            is_bloc = ouverture.bloc

            lead_allowed = (
                not is_bloc
                and salle
                and ouverture.relais in (salle.relais_en_tete or [])
            )

            seance_data = {
                "niveau": ouverture.niveau,
                "couleur": ouverture.couleur,
                "relais": ouverture.relais,

                # Moulinette / bloc
                "nb_try": s.nb_try,
                "nb_top": s.nb_top,
                "flash": s.flash,

                # Tête (si autorisée)
                "lead_allowed": lead_allowed,
                "nb_try_lead": s.nb_try_lead if lead_allowed else None,
                "nb_top_lead": s.nb_top_lead if lead_allowed else None,
                "flash_lead": s.flash_lead if lead_allowed else None,
            }

            key = "bloc" if is_bloc else "voie"
            salles_map[salle.nom if salle else gettext("Salle inconnue")][key].append(seance_data)

        # normalisation pour le template
        for salle_name, disciplines in salles_map.items():
            salles_data.append({
                "salle": salle_name,
                "voies": disciplines["voie"],
                "blocs": disciplines["bloc"],
            })

    # --------------------------------------------------
    # Construction du calendrier
    # --------------------------------------------------
    calendar_days = []

    start_weekday = first_day.weekday()  # 0 = lundi

    for _ in range(start_weekday):
        calendar_days.append(None)

    for d in range(1, days_in_month + 1):
        cell_date = date(year, month, d)

        calendar_days.append({
            "day": d,
            "has_seance": d in days_with_seance,
            "is_today": cell_date == today,
            "is_selected": cell_date == selected_date,
            "weekday": cell_date.weekday(),
        })

    # --------------------------------------------------
    # Navigation mois
    # --------------------------------------------------
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    context = {
        "climber": climber,

        "year": year,
        "month": month,
        "month_label": month_label,

        "calendar_days": calendar_days,
        "selected_date": selected_date,

        # Détails
        "salles_data": salles_data,

        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,

        "weekdays": [
            gettext("L"), gettext("M"), gettext("M"),
            gettext("J"), gettext("V"), gettext("S"), gettext("D")
        ],
    }

    return render(
        request,
        "staff_admin/training/calendar.html",
        context,
    )
