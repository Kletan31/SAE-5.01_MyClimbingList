# applications/core/utils/graph/profil_style.py

from django.db.models import Sum, Q
from datetime import datetime

import plotly.graph_objs as go
from django.utils.encoding import force_str
from django.utils.translation import gettext as _

from applications.core.models import Seance
from applications.core.utils.graph.profil_style_proportion import (
    calculate_quotient_distributions
)
from applications.core.utils.i18n.profil_style import (
    PROFILE_LABELS,
    STYLE_LABELS,
)
from applications.core.utils.i18n.normalize import nfc


# REGEX pour exclure les voies "découvertes" (3, 3+, 4, et 4+ inclus)
niveau_pattern = r"^[5-9]"


# ============================
# Fonction principale
# ============================

def profil_style_process_chart(
    user,
    viewport_height,
    viewport_width,
    bloc=False,
    field_name="profil",
    date_seance=None,
    salle_id=None,
):
    """
    Génère un graphique radar pour les blocs ou voies
    en fonction d'un champ (profil ou style).
    """

    date_seance = (
        datetime.strptime(date_seance, "%Y-%m-%d").date()
        if date_seance else None
    )
    salle_id = int(salle_id) if salle_id else None

    # Clés métier attendues
    raw_labels = get_labels(bloc, field_name)

    # Séances filtrées
    filtered_seances = get_filtered_seances(
        user, bloc, field_name, date_seance, salle_id
    )

    # Comptage brut (clé métier → nombre)
    item_counts = count_items(filtered_seances, field_name, raw_labels)

    # Distribution normalisée (clé métier conservée)
    distribution = calculate_quotient_distributions(
        user, bloc, field_name, date_seance, salle_id
    )

    preferred_profil_style = (
        None if salle_id else get_key_with_max_value(distribution)
    )

    percentages = calculate_percentages(distribution)

    # Labels traduits pour affichage
    labels, values = extract_labels_and_values(
        percentages,
        field_name,
    )

    trace = get_radar_trace(labels, values, field_name)
    layout = get_radar_layout(values, viewport_height, viewport_width)

    graph_json = go.Figure(data=[trace], layout=layout).to_json()

    return {
        "graph_json": graph_json,
        "percentage": percentages,
        "preferred": preferred_profil_style,
    }


# ============================
# Labels métier (clés DB)
# ============================

def get_labels(bloc, field_name):
    profil_label = ["dalle", "dièdre", "dévers", "toit", "vertical"]
    style_voie_label = ["conti", "rési", "bloc"]
    style_bloc_label = ["classic", "physic", "tricky", "coordo", "technic"]

    if field_name == "profil":
        return profil_label
    elif field_name == "style":
        return style_bloc_label if bloc else style_voie_label
    return []


# ============================
# Filtrage & comptage
# ============================

def get_filtered_seances(user, bloc, field_name, date_seance=None, salle_id=None):
    filter_kwargs = {
        f"ouverture__{field_name}__isnull": False,
        "user": user,
        "ouverture__bloc": bloc,
        "ouverture__niveau__regex": niveau_pattern,
    }

    if date_seance:
        filter_kwargs["date_seance"] = date_seance
        filter_kwargs["ouverture__salle_id"] = salle_id

    return (
        Seance.objects.filter(**filter_kwargs)
        .values("ouverture_id", f"ouverture__{field_name}", "ouverture__niveau")
        .annotate(
            total_top=Sum("nb_top"),
            total_top_lead=Sum("nb_top_lead"),
        )
        .filter(Q(total_top__gte=1) | Q(total_top_lead__gte=1))
    )


def count_items(filtered_seances, field_name, labels):
    counts = {label: 0 for label in labels}

    for seance in filtered_seances:
        item = seance[f"ouverture__{field_name}"]
        if item in counts:
            counts[item] += 1

    return counts


# ============================
# Calculs
# ============================

def get_key_with_max_value(dictionary):
    if not dictionary or all(value == 0 for value in dictionary.values()):
        return "undefined"
    return max(dictionary, key=dictionary.get)


def calculate_percentages(data):
    """
    IMPORTANT :
    - on NE slugifie PAS
    - on conserve les clés métier originales (avec accents)
    """
    total = sum(data.values())
    if total == 0:
        return {key: 0 for key in data}

    return {
        key: round((value / total) * 100)
        for key, value in data.items()
    }


# ============================
# Labels affichés (i18n)
# ============================

def extract_labels_and_values(data, field_name):
    """
    - mapping FR
    - normalisation NFC
    - traduction gettext
    - force_str pour Plotly / JSON
    """
    mapping = PROFILE_LABELS if field_name == "profil" else STYLE_LABELS

    labels = [
        force_str(_(nfc(mapping.get(key, key))))
        for key in data.keys()
    ]
    values = list(data.values())

    return labels, values


# ============================
# Plotly
# ============================

def get_radar_trace(labels, values, field_name):
    # fermer le radar
    labels.append(labels[0])
    values.append(values[0])

    if field_name == "style":
        line_color = "#951B95"
        fill_color = "rgba(149, 27, 149, 0.3)"
    else:
        line_color = "#FFB514"
        fill_color = "rgba(255, 181, 20, 0.3)"

    return go.Scatterpolar(
        r=values,
        theta=labels,
        fill="toself",
        line=dict(color=line_color, width=1),
        fillcolor=fill_color,
    )


def get_radar_layout(values, viewport_height, viewport_width):
    return {
        "polar": {
            "bgcolor": "rgb(250, 250, 250)",
            "radialaxis": {
                "range": [0, max(max(values) * 1.05, 1)],
                "visible": False,
            },
            "angularaxis": {
                "gridcolor": "#c2c2c2",
                "rotation": 90,
                "tickfont": {
                    "size": 11,
                    "color": "black",
                    "weight": "bold",
                },
            },
        },
        "showlegend": False,
        "height": viewport_height * 0.45,
        "margin": {
            "t": viewport_height * 0.05,
            "b": viewport_height * 0.05,
            "r": viewport_width * 0.125,
            "l": viewport_width * 0.125,
        },
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    }
