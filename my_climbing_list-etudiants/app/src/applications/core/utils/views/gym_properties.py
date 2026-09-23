from applications.core.models import Ouverture
import plotly.graph_objs as go
from django.db.models import Count, F, Q
from django.db.models.functions import Round
from plotly.graph_objects import Figure


def prepare_gym_graph(salle, bloc, viewport_height, profil=None, style=None):
    """
    Prépare les données, les statistiques et le graphique pour une salle donnée.

    :param salle: Instance du modèle Salle
    :param bloc: Booléen indiquant si c'est du bloc ou de la voie
    :param viewport_height: Hauteur de la fenêtre d'affichage
    :param profil: Liste des profils sélectionnés.
    :param style: Liste des styles sélectionnés.
    :return: Dictionnaire contenant les données statistiques et le graphique Plotly
    """
    # Constantes
    FIXED_PROFILS = ["dalle", "dièdre", "vertical", "dévers", "toit"]
    FIXED_STYLES = ["conti", "rési", "bloc", "classic", "technic", "physic", "coordo", "tricky"]

    # Étape 1 : Filtrer les ouvertures
    ouvertures = filter_ouvertures(salle, bloc, profil, style)

    # Étape 2 : Calculs statistiques globaux
    stats_globaux = calculate_global_stats(ouvertures, salle)

    # Étape 3 : Calcul des statistiques par profil et style
    profils_stats = calculate_stats(ouvertures, FIXED_PROFILS, "profil", stats_globaux["total_ouvertures"])
    styles_stats = calculate_stats(ouvertures, FIXED_STYLES, "style", stats_globaux["total_ouvertures"])

    # Étape 4 : Calcul deu détails des ouvertures
    ouvertures, niveaux = count_ouvertures(ouvertures, salle.relais_en_tete)

    # Étape 5 : Génération du graphique Plotly
    graph_json = generate_graph(ouvertures, niveaux, viewport_height)

    # Résultat final
    return {
        "graph": graph_json,
        "total_ouvertures": stats_globaux["total_ouvertures"],
        "total_moulinette": stats_globaux["total_moulinette"],
        "total_tete": stats_globaux["total_tete"],
        "profils_stats": profils_stats,
        "styles_stats": styles_stats,
    }


def filter_ouvertures(salle, bloc, profil, style):
    """
    Filtre les ouvertures en fonction des critères.

    :return: QuerySet d'ouvertures filtrées
    """
    ouvertures = Ouverture.objects.filter(active=True, salle=salle, bloc=bloc)
    if profil:
        ouvertures = ouvertures.filter(profil__in=profil)
    if style:
        ouvertures = ouvertures.filter(style__in=style)
    return ouvertures


def calculate_global_stats(ouvertures, salle):
    """
    Calcule les statistiques globales.

    :return: Dictionnaire des statistiques globales
    """
    total_ouvertures = ouvertures.count()
    total_moulinette = ouvertures.exclude(relais__in=salle.relais_en_tete).count()
    total_tete = ouvertures.filter(relais__in=salle.relais_en_tete).count()

    return {
        "total_ouvertures": total_ouvertures,
        "total_moulinette": total_moulinette,
        "total_tete": total_tete,
    }


def calculate_stats(ouvertures, fixed_keys, field_name, total_ouvertures):
    """
    Calcule les statistiques (totaux et pourcentages) pour un champ donné.

    :param ouvertures: QuerySet d'ouvertures
    :param fixed_keys: Liste des clés fixes (profils ou styles)
    :param field_name: Nom du champ à analyser ("profil" ou "style")
    :param total_ouvertures: Total d'ouvertures pour calculer les pourcentages
    :return: Liste de statistiques pour les clés fixes
    """
    stats_raw = (
        ouvertures.exclude(Q(**{f"{field_name}__isnull": True}))
        .values(field_name)
        .annotate(total=Count(field_name))
        .annotate(percentage=Round(F("total") * 100.0 / total_ouvertures))
    )

    stats = [{field_name: key, "total": 0, "percentage": 0} for key in fixed_keys]

    for raw in stats_raw:
        for stat in stats:
            if stat[field_name] == raw[field_name]:
                stat["total"] = raw["total"]
                stat["percentage"] = raw["percentage"]
                break

    return stats


def generate_graph(ouvertures, niveaux, viewport_height):
    """
    Génère un graphique Plotly.

    :return: JSON du graphique
    """
    plotly_data, plotly_layout = generate_plotly_data_and_layout(ouvertures, niveaux, viewport_height)
    fig = Figure(data=plotly_data, layout=plotly_layout)
    return fig.to_json()


def count_ouvertures(ouvertures, relais_en_tete):
    """
    Compte les réalisations en moulinette et en tête par niveau.

    :param ouvertures: Queryset des ouvertures filtrées.
    :param relais_en_tete: Liste des relais disponibles pour les ascensions en tête.
    :return: Tuple (dictionnaire des statistiques par niveau, liste des niveaux triés).
    """
    # Définir les niveaux de base attendus
    niveaux_base = ['5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b', '7c', '8a', '8b', '8c', '9a', '9b', '9c']

    # Initialiser un dictionnaire pour les statistiques par niveau
    stats_ouvertures = {niveau: {'moulinette': 0, 'lead': 0} for niveau in niveaux_base}

    # Parcourir les ouvertures
    for ouverture in ouvertures:
        niveau = ouverture.niveau[:2]  # Extraire le niveau (e.g., '5a')
        if niveau in niveaux_base:  # Éviter les cotations "enfant", "3+" et autre
            if ouverture.relais in relais_en_tete:  # Si le relais est dans les relais disponibles pour la tête
                stats_ouvertures[niveau]['lead'] += 1
            else:  # Sinon, compter comme moulinette
                stats_ouvertures[niveau]['moulinette'] += 1

    # Retourner les statistiques et la liste triée des niveaux
    return stats_ouvertures, niveaux_base


# noinspection DuplicatedCode
def generate_plotly_data_and_layout(ouvertures, niveaux, viewport_height):
    """Génère les données et le layout pour un graphique Plotly."""
    # Déterminer la valeur maximale des réalisations pour ajuster l'axe Y
    max_value = max([value['moulinette'] + value['lead'] for value in ouvertures.values()])
    # Ajuster la borne supérieure à une valeur légèrement supérieure pour un peu d'espace
    upper_bound = max_value + 3 if max_value + 3 > 10 else 10  # Ajouter 3 pour laisser un peu de marge au-dessus

    classiques = [ouvertures[niveau]['moulinette'] for niveau in niveaux]
    leads = [ouvertures[niveau]['lead'] for niveau in niveaux]

    plotly_data = [
        go.Bar(
            x=niveaux,
            y=leads,
            name='En tête',
            marker=dict(color='rgb(175, 213, 75)'),
            width=0.5,
        ),
        go.Bar(
            x=niveaux,
            y=classiques,
            name='Moulinette',
            marker=dict(color='rgb(60, 78, 148)'),
            width=0.5,
        ),
    ]

    plotly_layout = {
        'autosize': True,
        'showlegend': False,
        'barmode': 'stack',
        'height': viewport_height * 0.45,
        'margin': {
            'l': 0,
            'r': 13,
            'b': 0,
            't': 0,
            'pad': 5
        },
        'xaxis': {
            'title': '',
            'showgrid': False,
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': 'black',
                'weight': 'bold',
            },
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': 'rgba(200, 200, 200, 0.5)',
            'showticklabels': True,
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 12,
                'color': 'black',
            },
            'fixedrange': True,
            'range': [0, upper_bound],  # Ajuster la plage en fonction des niveaux réels
        },
        'hovermode': False,
        'dragmode': False,
        'barcornerradius': 0,
        'plot_bgcolor': 'rgba(0,0,0,0)',
    }

    return plotly_data, plotly_layout
