from collections import defaultdict
from datetime import date
from applications.core.models import Seance

# REGEX pour exclure les voies "découvertes"
niveau_pattern = r'^[3-9]'


# noinspection PyTypeChecker
def get_user_projects(user):
    seances = (Seance.objects
               .filter(user=user, ouverture__niveau__regex=niveau_pattern)
               .select_related('ouverture', 'ouverture__salle'))

    projets_temp = defaultdict(lambda: {
        'total_try_moulinette': 0,
        'total_try_lead': 0,
        'total_top': 0,
        'total_top_lead': 0,
        'last_try_date': None,   # type: date | None
        'last_seance': None,     # type: Seance | None
    })

    for seance in seances:
        ouverture_id = seance.ouverture_id
        data = projets_temp[ouverture_id]

        data['total_try_moulinette'] += seance.nb_try
        data['total_try_lead'] += seance.nb_try_lead
        data['total_top'] += seance.nb_top
        data['total_top_lead'] += seance.nb_top_lead

        if data['last_try_date'] is None or seance.date_seance > data['last_try_date']:
            data['last_try_date'] = seance.date_seance
            data['last_seance'] = seance

    projets = []

    for ouverture_id, data in projets_temp.items():
        last_seance = data['last_seance']
        # ✅ Guard de type : PyCharm sait que la suite manipule une Seance
        if not isinstance(last_seance, Seance):
            continue
        if not last_seance.is_project_visible:
            continue

        ouverture = last_seance.ouverture
        if not ouverture.active:
            continue

        total_try = data['total_try_moulinette']
        total_try_lead = data['total_try_lead']
        total_top = data['total_top']
        total_top_lead = data['total_top_lead']

        salle = ouverture.salle
        relais_en_tete = salle.relais_en_tete or []
        voie_peut_etre_faite_en_tete = ouverture.relais in relais_en_tete

        # Cas 1 : voie grimpable en tête et déjà topée en tête → pas un projet
        if voie_peut_etre_faite_en_tete and total_top_lead > 0:
            continue

        # Cas 2 : au moins une montée
        if total_try == 0 and total_try_lead == 0:
            continue

        # Cas 3 : garder si grimpable en tête (pas topée en tête par cas 1)
        #         ou si non-grimpable en tête ET non topée en moulinette
        if voie_peut_etre_faite_en_tete or total_top == 0:
            projets.append({
                'ouverture_id': ouverture.id,
                'bloc': ouverture.bloc,
                'leadable': voie_peut_etre_faite_en_tete,
                'nom': ouverture.nom,
                'couleur': ouverture.couleur,
                'salle': ouverture.salle,
                'niveau': ouverture.niveau,
                'niveau_couleur': ouverture.niveau_couleur,
                'style': ouverture.style,
                'profil': ouverture.profil,
                'relais': ouverture.relais,
                'date_ouverture': ouverture.date_ouverture,
                'last_try_date': data['last_try_date'],
                'total_try_moulinette': total_try,
                'total_top_moulinette': total_top,
                'total_try_lead': total_try_lead,
            })

    return projets
