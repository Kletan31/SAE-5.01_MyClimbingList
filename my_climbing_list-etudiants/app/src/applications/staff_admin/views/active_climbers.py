# applications/staff_admin/views/active_climbers.py

from datetime import timedelta, date as date_cls

from django.shortcuts import render
from applications.staff_admin.decorators import staff_required
from django.utils.timezone import now
from django.db.models import Max, Min
from django.contrib.auth import get_user_model

from applications.core.models import Seance
from applications.staff_admin.models import ClimberLevelDaily
from applications.staff_admin.utils import get_salle_from_request

User = get_user_model()


@staff_required
def active_climbers_view(request):
    """
    Grimpeurs actifs sur les 30 derniers jours
    dans la salle associée au compte staff.

    Le niveau Elo affiché est GLOBAL (homogène inter-salles).
    """

    salle = get_salle_from_request(request)
    bloc = request.GET.get("bloc") == "1"

    # =====================================================
    # Date de référence
    # =====================================================
    today = now().date()
    max_date = today - timedelta(days=1)  # 👈 VEILLE UNIQUEMENT

    date_str = request.GET.get("date")

    try:
        selected_date = (
            date_cls.fromisoformat(date_str)
            if date_str else max_date
        )
    except ValueError:
        selected_date = max_date

    # Sécurité : jamais au-delà de la veille
    if selected_date > max_date:
        selected_date = max_date

    # =====================================================
    # Bornes de dates disponibles (globales)
    # =====================================================
    date_bounds = ClimberLevelDaily.objects.filter(
        bloc=bloc,
    ).aggregate(
        min_date=Min("date"),
        max_date=Max("date"),
    )

    min_date = date_bounds["min_date"]

    # =====================================================
    # Navigation par dates
    # =====================================================
    prev_date = selected_date - timedelta(days=1)
    next_date = selected_date + timedelta(days=1)

    if not min_date or prev_date < min_date:
        prev_date = None

    # ❗ Bloqué à la veille
    if next_date > max_date:
        next_date = None

    # =====================================================
    # Grimpeurs actifs dans LA SALLE (30 derniers jours)
    # =====================================================
    date_min_activity = today - timedelta(days=30)

    recent_users = (
        Seance.objects
        .filter(
            ouverture__salle=salle,
            ouverture__bloc=bloc,
            date_seance__gte=date_min_activity,
        )
        .values("user")
        .annotate(last_passage=Max("date_seance"))
        .order_by("-last_passage")
    )

    # =====================================================
    # Niveaux ELO globaux à la date sélectionnée
    # =====================================================
    levels_today = {
        lvl.user_id: lvl
        for lvl in ClimberLevelDaily.objects.filter(
            bloc=bloc,
            date=selected_date,
        )
    }

    # =====================================================
    # Construction des grimpeurs
    # =====================================================
    climbers = []

    users_by_id = {
        u.id: u
        for u in User.objects.filter(
            id__in=[u["user"] for u in recent_users]
        )
    }

    for entry in recent_users:
        user_id = entry["user"]
        last_passage = entry["last_passage"]

        user = users_by_id.get(user_id)
        level_obj = levels_today.get(user_id)

        climbers.append({
            "user": user,
            "elo": level_obj.elo if level_obj else None,
            "level": level_obj.level if level_obj else "-",
            "color": level_obj.color if level_obj else "#333",
            "elo_trend": level_obj.elo_trend if level_obj else None,
            "last_passage": last_passage,
        })

    # =====================================================
    # Tri principal : ELO décroissant
    # =====================================================
    climbers.sort(
        key=lambda c: c["elo"] if c["elo"] is not None else -1,
        reverse=True,
    )

    # =====================================================
    # Contexte template
    # =====================================================
    context = {
        "salle": salle,
        "climbers": climbers,
        "bloc": bloc,

        # Dates
        "selected_date": selected_date,
        "prev_date": prev_date,
        "next_date": next_date,
        "min_date": min_date,
        "today": today,
    }

    return render(
        request,
        "staff_admin/active_climbers/active_climbers.html",
        context
    )
