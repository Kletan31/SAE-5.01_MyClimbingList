# applications/core/views/graph.py

from django.shortcuts import render
from applications.core.decorators import non_staff_required
from django.utils.translation import get_language
from applications.core.utils import progression_process_chart, ascension_process_chart, profil_style_process_chart


@non_staff_required
def graph_view(request):
    user = request.user
    vh = request.session.get('viewport_height', 800)
    vw = request.session.get('viewport_width', 400)
    lang = get_language()

    # Générer les graphiques de progression
    progression_data = {
        'voie': progression_process_chart(user, bloc=False, viewport_height=vh),
        'bloc': progression_process_chart(user, bloc=True, viewport_height=vh),
    }

    # Générer les graphiques de réalisation
    ascension_data = {
        'voie': ascension_process_chart(user, viewport_height=vh, bloc=False),
        'bloc': ascension_process_chart(user, viewport_height=vh, bloc=True),
        'voie_flash': ascension_process_chart(user, flash_filter=True, viewport_height=vh, bloc=False),
        'bloc_flash': ascension_process_chart(user, flash_filter=True, viewport_height=vh, bloc=True),
    }

    # Générer les graphiques de profils
    profil_data = {
        'voie': profil_style_process_chart(user, viewport_height=vh, viewport_width=vw, bloc=False, field_name='profil'),
        'bloc': profil_style_process_chart(user, viewport_height=vh, viewport_width=vw, bloc=True, field_name='profil'),
    }

    # Générer les graphiques de style
    style_data = {
        'voie': profil_style_process_chart(user, viewport_height=vh, viewport_width=vw, bloc=False, field_name='style'),
        'bloc': profil_style_process_chart(user, viewport_height=vh, viewport_width=vw, bloc=True, field_name='style'),
    }

    # Préparer le contexte
    context = {
        # Progression
        'graph_progression_voie': progression_data['voie']['graph_json'],
        'level_voie': progression_data['voie']['user_level'],
        'level_voie_color': progression_data['voie']['user_level_color'],

        'graph_progression_bloc': progression_data['bloc']['graph_json'],
        'level_bloc': progression_data['bloc']['user_level'],
        'level_bloc_color': progression_data['bloc']['user_level_color'],

        # Ascension
        'graph_ascension_voie': ascension_data['voie']['graph_json'],
        'total_moulinette_voie': ascension_data['voie']['total_moulinette'],
        'total_lead_voie': ascension_data['voie']['total_lead'],

        'graph_ascension_bloc': ascension_data['bloc']['graph_json'],
        'total_bloc': ascension_data['bloc']['total_moulinette'],

        'graph_ascension_voie_flash': ascension_data['voie_flash']['graph_json'],
        'total_moulinette_voie_flash': ascension_data['voie_flash']['total_moulinette'],
        'total_lead_voie_flash': ascension_data['voie_flash']['total_lead'],

        'graph_ascension_bloc_flash': ascension_data['bloc_flash']['graph_json'],
        'total_bloc_flash': ascension_data['bloc_flash']['total_moulinette'],

        # Graphiques de profils
        'graph_profil_voie': profil_data['voie']['graph_json'],
        'profil_percentage_voie': profil_data['voie']['percentage'],
        'profil_preferred_voie': profil_data['voie']['preferred'],

        'graph_profil_bloc': profil_data['bloc']['graph_json'],
        'profil_percentage_bloc': profil_data['bloc']['percentage'],
        'profil_preferred_bloc': profil_data['bloc']['preferred'],

        # Graphiques de styles
        'graph_style_voie': style_data['voie']['graph_json'],
        'style_percentage_voie': style_data['voie']['percentage'],
        'style_preferred_voie': style_data['voie']['preferred'],

        'graph_style_bloc': style_data['bloc']['graph_json'],
        'style_percentage_bloc': style_data['bloc']['percentage'],
        'style_preferred_bloc': style_data['bloc']['preferred'],
    }

    return render(request, 'core/graph/graph.html', context)
