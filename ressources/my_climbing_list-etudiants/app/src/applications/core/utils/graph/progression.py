from datetime import datetime, timedelta

import plotly.graph_objs as go
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.utils.encoding import force_str

from applications.staff_admin.models import ClimberLevelDaily
# Attention aux imports circulaires
from applications.core.utils.i18n.month import MONTHS_SHORT


# ============================
# Fonction principale
# ============================

def progression_process_chart(user, bloc, viewport_height):
    """
    Génère le graphique de progression à partir des données
    ClimberLevelDaily déjà calculées en base.
    """

    qs = (
        ClimberLevelDaily.objects
        .filter(user=user, bloc=bloc, elo__isnull=False)
        .order_by("date")
    )

    if not qs.exists():
        return {
            "graph_json": empty_graph(viewport_height),
            "user_level": "-",
            "user_level_color": "#333",
        }

    timestamps, elos = prepare_graph_data(qs)

    trace = create_plotly_trace(timestamps, elos)
    layout = configure_plotly_layout(qs, viewport_height)

    graph_json = go.Figure(data=[trace], layout=layout).to_json()

    last = qs.last()

    return {
        "graph_json": graph_json,
        "user_level": last.level,
        "user_level_color": last.color,
    }


# ============================
# Préparation des données
# ============================

def prepare_graph_data(qs):
    """
    Génère une série continue jour par jour à partir des
    valeurs journalières stockées en base.
    """

    values_by_date = {row.date: row.elo for row in qs}

    start_date = qs.first().date
    end_date = now().date()

    all_dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    elos = []
    last_known = None

    for d in all_dates:
        if d in values_by_date:
            last_known = values_by_date[d]
        elos.append(last_known)

    timestamps = [
        datetime.combine(d, datetime.min.time()).timestamp() * 1000
        for d in all_dates
    ]

    return timestamps, elos


# ============================
# Plotly
# ============================

def create_plotly_trace(timestamps, elos):
    return go.Scatter(
        x=timestamps,
        y=elos,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(238, 127, 0, 0.4)",
        line=dict(color="#EE7F00", width=2, shape="spline"),
        name=_("Progression"),
    )


def configure_plotly_layout(qs, viewport_height):
    start_date = qs.first().date
    last_date = qs.last().date

    # On garantit au moins un an d’affichage
    end_date = max(start_date + timedelta(days=365), last_date)

    tickvals, ticktext = calculate_ticks(start_date, end_date)

    return {
        "height": viewport_height * 0.45,
        "margin": {"l": 0, "r": 13, "b": 0, "t": 0, "pad": 5},
        "yaxis": {
            "tickvals": [1000, 1300, 1600, 1900, 2200],
            "ticktext": ["5", "6", "7", "8", "9"],
            "range": [994, 2400],
            "fixedrange": True,
            "showgrid": True,
            "gridcolor": "lightgrey",
        },
        "xaxis": {
            "range": [
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
            ],
            "type": "date",
            "tickvals": tickvals,
            "ticktext": ticktext,
            "showgrid": False,
        },
        "plot_bgcolor": "white",
        "paper_bgcolor": "white",
        "showlegend": False,
    }


# ============================
# Gestion des ticks temporels
# ============================

def calculate_ticks(start_date, end_date):
    total_days = (end_date - start_date).days
    total_years = total_days / 365.25

    # ---------------------------------
    # Détermination des positions
    # ---------------------------------

    if total_years <= 1:
        # Cas < 1 an : 5 repères "mois"
        fractions = (1 / 12, 3.5 / 12, 6 / 12, 8.5 / 12, 11 / 12)

    else:
        # Cas > 1 an : au moins 4 labels,
        # jamais au début ni à la fin
        fractions = (1 / 5, 2 / 5, 3 / 5, 4 / 5)

    # ---------------------------------
    # Calcul des dates
    # ---------------------------------

    tick_dates = [
        start_date + timedelta(days=total_days * f)
        for f in fractions
    ]

    tickvals = [
        datetime.combine(d, datetime.min.time()).timestamp() * 1000
        for d in tick_dates
    ]

    # ---------------------------------
    # Labels i18n
    # ---------------------------------

    if total_years > 1:
        ticktext = [
            f"{force_str(MONTHS_SHORT[d.month])} {str(d.year)[-2:]}"
            for d in tick_dates
        ]
    else:
        ticktext = [
            force_str(MONTHS_SHORT[d.month])
            for d in tick_dates
        ]

    return tickvals, ticktext


# ============================
# Fallback
# ============================

def empty_graph(viewport_height):
    fig = go.Figure()
    fig.update_layout(
        height=viewport_height * 0.45,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            dict(
                text=_("No data available"),
                x=0.5,
                y=0.5,
                showarrow=False,
                xref="paper",
                yref="paper",
            )
        ],
    )
    return fig.to_json()
