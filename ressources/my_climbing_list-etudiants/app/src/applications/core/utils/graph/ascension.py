from applications.core.models import Seance
from django.db.models import Sum, Q
import plotly.graph_objs as go

# REGEX pour exclure les voies "découvertes" (3, 3+, 4, et 4+ inclus)
niveau_pattern = r'^[5-9]'


# Protocole de création de graphique
def ascension_process_chart(user, bloc, viewport_height, flash_filter=False, date_seance=None, salle_id=None):
    # Déterminer l'échelle appropriée
    details_view = True if date_seance and salle_id else False

    # Récupérer les séances filtrées par utilisateur et type (voie/bloc)
    seances = get_filtered_seances(user, bloc, flash_filter, date_seance, salle_id)

    # Compter les réalisations par niveau
    ascensions, niveaux = count_ascensions(seances)

    # Créer les données pour Plotly
    data = create_plotly_data(ascensions, niveaux)

    # Générer le layout pour le graphique
    layout_ascension = generate_plotly_layout(ascensions, viewport_height, details_view)

    # Convertir le graphique en JSON pour être utilisé dans le template
    graph_json = go.Figure(data=data, layout=layout_ascension).to_json()

    # Calculer les totaux
    total_moulinette = sum(value['moulinette'] for value in ascensions.values())
    total_lead = sum(value['lead'] for value in ascensions.values())

    # Retourner le JSON du graphique ainsi que les totaux
    return {
        'graph_json': graph_json,
        'total_moulinette': total_moulinette,
        'total_lead': total_lead,
    }


# Filtre les séances de l'utilisateur
def get_filtered_seances(user, bloc, flash_filter, date_seance, salle_id):
    """
    Filtre les séances de l'utilisateur, les groupe par ouverture_id et calcule
    la somme de nb_top et nb_top_lead pour chaque groupe.
    """
    # Filtrer les séances par utilisateur et type (bloc/voie)
    seances = Seance.objects.filter(user=user, ouverture__bloc=bloc, ouverture__niveau__regex=niveau_pattern)

    # Filtrer les séances avec flash=True OU flash_lead=True si activé
    if flash_filter:
        seances = seances.filter(Q(flash=True) | Q(flash_lead=True))

    # Filtrer les séances par date [details_view]
    if date_seance:
        seances = seances.filter(date_seance=date_seance)

    # Filtrer les séances par salle [details_view]
    if salle_id:
        seances = seances.filter(ouverture__salle_id=salle_id)

    # Grouper par ouverture_id et calculer les sommes
    seances = seances.values('ouverture_id', 'ouverture__niveau').annotate(
        total_top=Sum('nb_top'),
        total_top_lead=Sum('nb_top_lead')
    )

    return seances


# Compte les réalisations en moulinette et en tête
def count_ascensions(seances):
    # Liste des niveaux utilisés pour les cotations des voies/blocs
    niveaux_base = ['5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b', '7c', '8a', '8b', '8c', '9a', '9b', '9c']

    # Initialiser un dictionnaire pour compter les réalisations par niveau
    ascensions = {niveau: {'moulinette': 0, 'lead': 0} for niveau in niveaux_base}

    # Parcourir les séances et compter les ascensions
    for seance in seances:
        niveau = seance['ouverture__niveau'][:2]  # Récupérer le niveau (e.g., '5a')
        if niveau in niveaux_base:
            # Ajouter les réalisations moulinette et en tête
            if seance['total_top_lead'] > 0:
                ascensions[niveau]['lead'] += 1
            else:
                ascensions[niveau]['moulinette'] += 1 if seance['total_top'] > 0 else 0

    return ascensions, niveaux_base


# Crée les objets de données pour Plotly
def create_plotly_data(ascensions, niveaux):
    # Créer les barres pour les réalisations en moulinette et en tête
    classiques = [ascensions[niveau]['moulinette'] for niveau in niveaux]
    leads = [ascensions[niveau]['lead'] for niveau in niveaux]

    trace_leads = go.Bar(
        x=niveaux,
        y=leads,
        name='En tête',
        marker=dict(color='rgb(175, 213, 75)'),
        width=0.5,
    )

    trace_classiques = go.Bar(
        x=niveaux,
        y=classiques,
        name='Moulinette',
        marker=dict(color='rgb(60, 78, 148)'),
        width=0.5,
    )

    return [trace_leads, trace_classiques]


# Génère la configuration du layout pour Plotly avec ajustement dynamique
def generate_plotly_layout(ascensions, viewport_height, details_view=False):
    # Déterminer la valeur maximale des réalisations pour ajuster l'axe Y
    max_value = max([value['moulinette'] + value['lead'] for value in ascensions.values()])

    # Ajuster la borne supérieure à une valeur légèrement supérieure pour un peu d'espace
    if details_view:
        upper_bound = max_value + 3.5 if max_value + 3 > 5 else 5.5  # Ajouter 3 pour laisser un peu de marge au-dessus
    else:
        upper_bound = max_value + 3.5 if max_value + 3 > 11 else 11.5  # Ajouter 3 pour laisser un peu de marge au-dessus

    # Créer une copie adaptée de `layout_plotly`
    layout_ascension = {
        'showlegend': False,
        'barmode': 'stack',
        'height': viewport_height*0.43,
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
            }
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
            'fixedrange': True,  # Désactiver le zoom sur l'axe Y
            'range': [0, upper_bound],  # Ajuster la plage en fonction des niveaux réels
        },
        'hovermode': False,
        'dragmode': False,
        'barcornerradius': 0,
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
    }

    return layout_ascension
