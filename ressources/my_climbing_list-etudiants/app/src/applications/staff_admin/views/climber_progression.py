# applications/staff_admin/views/climber_progression.py

from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from applications.staff_admin.decorators import staff_required
from django.contrib.auth import get_user_model
from django.urls import reverse

import plotly.graph_objects as go
from plotly.offline import plot

from applications.staff_admin.models import ClimberLevelDaily
from applications.staff_admin.utils import get_salle_from_request, elo2cotation

User = get_user_model()


# =====================================================
# Repères Elo → cotations (AXE Y)
# =====================================================

ELO_TICKS = [
    1000, 1100, 1200,
    1300, 1400, 1500,
    1600, 1700, 1800,
    1900, 2000, 2100,
    2200,
]

COTATION_TICKS = [
    "5a", "5b", "5c",
    "6a", "6b", "6c",
    "7a", "7b", "7c",
    "8a", "8b", "8c",
    "9a",
]


@staff_required
def climber_progression_view(request, user_id):
    """
    Progression Elo globale d’un grimpeur.

    - Courbe continue (sans points)
    - Axe Y gradué en cotations
    - Hover : cotation + Elo
    """

    # -----------------------------
    # URL de retour (ROBUSTE)
    # -----------------------------
    next_url = request.GET.get("next")

    if not next_url:
        next_url = request.META.get("HTTP_REFERER")

    if not next_url:
        next_url = reverse("staff_admin:active_climbers")

    # -----------------------------
    # Discipline
    # -----------------------------
    bloc = request.GET.get("bloc") == "1"

    # -----------------------------
    # Salle du staff (contexte UI)
    # -----------------------------
    salle = get_salle_from_request(request)

    # -----------------------------
    # Grimpeur
    # -----------------------------
    user = get_object_or_404(User, id=user_id)

    # -----------------------------
    # Historique Elo GLOBAL
    # -----------------------------
    levels = (
        ClimberLevelDaily.objects
        .filter(
            user=user,
            bloc=bloc,
            elo__isnull=False,
        )
        .order_by("date")
    )

    graph_html = None

    if levels.exists():
        dates = [lvl.date for lvl in levels]
        elos = [lvl.elo for lvl in levels]
        cotations = [elo2cotation(e) for e in elos]

        # -----------------------------
        # Buffer temporel (visuel)
        # -----------------------------
        start_date = dates[0]
        end_date = dates[-1]
        total_days = (end_date - start_date).days or 1

        future_buffer = max(
            timedelta(days=3),
            timedelta(days=int(total_days * 0.1)),
        )

        # -----------------------------
        # Figure Plotly
        # -----------------------------
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=elos,
            mode="lines",
            line=dict(width=2),
            name="Progression",
            customdata=cotations,
            hovertemplate=(
                "Date : %{x}<br>"
                "Niveau : %{customdata}<br>"
                "Elo : %{y:.0f}"
                "<extra></extra>"
            ),
        ))

        fig.update_layout(
            margin=dict(l=40, r=20, t=30, b=40),
            height=400,
            hovermode="x unified",
            template="plotly_white",

            xaxis=dict(
                title="Date",
                range=[start_date, end_date + future_buffer],
            ),

            yaxis=dict(
                title="Niveau",
                range=[990, 2210],
                tickvals=ELO_TICKS,
                ticktext=COTATION_TICKS,
                fixedrange=False,
            ),
        )

        graph_html = plot(
            fig,
            output_type="div",
            include_plotlyjs=False,
        )

    # -----------------------------
    # Contexte template
    # -----------------------------
    context = {
        "salle": salle,
        "user": user,
        "bloc": bloc,
        "graph_html": graph_html,
        "next_url": next_url,
    }

    return render(
        request,
        "staff_admin/active_climbers/climber_progression.html",
        context
    )
