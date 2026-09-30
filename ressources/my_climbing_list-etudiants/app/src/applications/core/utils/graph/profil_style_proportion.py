from django.db.models import Q
from applications.core.models import Seance, Ouverture
from collections import defaultdict
from copy import deepcopy

###############
# Constantes  #
###############

# Définition des profils et styles possibles pour les blocs et les voies
DISTRIBUTIONS = {
    'profil': {'dalle': 0, 'dièdre': 0, 'dévers': 0, 'toit': 0, 'vertical': 0},
    'style_bloc': {'classic': 0, 'physic': 0, 'tricky': 0, 'coordo': 0, 'technic': 0},
    'style_voie': {'conti': 0, 'rési': 0, 'bloc': 0}
}

# REGEX pour exclure les voies "découvertes" (3, 3+, 4, et 4+ inclus)
niveau_pattern = r'^[5-9]'

###############
# Utilitaires #
###############


def initialize_distributions(bloc, field_name):
    """
    Initialise les distributions pour les profils ou les styles.
    Permet de partir d'une base neutre (valeurs initiales à 0).
    """
    if field_name == 'profil':
        return deepcopy(DISTRIBUTIONS['profil'])
    return deepcopy(DISTRIBUTIONS['style_bloc']) if bloc else deepcopy(DISTRIBUTIONS['style_voie'])


def calculate_distributions(data, bloc, field_name):
    """
    Calcule les proportions pour les profils ou les styles à partir des données fournies.
    """
    # Initialiser la distribution avec des valeurs par défaut
    distribution = initialize_distributions(bloc, field_name)

    # Compter les occurrences des champs spécifiés (profil ou style)
    for _, value in data:
        if value in distribution:
            distribution[value] += 1

    # Calculer la somme totale
    total = sum(distribution.values())

    # Calculer les proportions en évitant les divisions par zéro
    return {key: value / total if total > 0 else 0 for key, value in distribution.items()}


######################
# Logique principale #
######################


def get_salle_success_proportions(user, bloc):
    """
    Associe à chaque salle une proportion en fonction des succès de l'utilisateur dans celle-ci.
    """
    filter_kwargs = {
        "user": user,
        "ouverture__bloc": bloc,
        "ouverture__niveau__regex": niveau_pattern,
    }

    # Filtrer les séances de l'utilisateur et exclure les niveaux non pertinents
    successful_openings = (
        Seance.objects.filter(**filter_kwargs)  # Appliquer d'abord les filtres normaux
        .filter(Q(nb_top__gt=0) | Q(nb_top_lead__gt=0))  # Appliquer ensuite les conditions OR
        .values_list('ouverture__id', 'ouverture__salle__id')
        .distinct()
    )

    # Calculer le total des succès toutes salles confondues
    total_success_all = len(successful_openings)
    if total_success_all == 0:
        return {}

    # Compter les succès par salle
    salle_success_dict = defaultdict(int)
    for _, salle_id in successful_openings:
        salle_success_dict[salle_id] += 1

    # Calculer les proportions pondérées
    return {
        salle_id: total / total_success_all
        for salle_id, total in salle_success_dict.items()
    }


def calculate_field_distributions(salle_id, bloc, field_name):
    """
    Calcule les proportions pour un champ donné (profil ou style) dans une salle donnée.
    """
    data = (
        Ouverture.objects.filter(salle_id=salle_id, bloc=bloc, niveau__regex=niveau_pattern)
        .values_list('id', field_name)
    )

    return calculate_distributions(data, bloc, field_name)


def global_user_distribution(user, bloc, field_name, salle_id=None):
    """
    Calcule les proportions globales d'un champ (profil ou style) pondérées par les proportions de succès de
    l'utilisateur.
    """
    global_distribution = initialize_distributions(bloc, field_name)
    salle_success_proportions = get_salle_success_proportions(user, bloc)

    if salle_id:
        return calculate_field_distributions(salle_id, bloc, field_name)

    for salle_id, proportion in salle_success_proportions.items():
        local_distribution = calculate_field_distributions(salle_id, bloc, field_name)
        for key in global_distribution:
            global_distribution[key] += proportion * local_distribution[key]

    return global_distribution


def calculate_user_success_distribution(user, bloc, field_name, date_seance=None, salle_id=None):
    """
    Récupère les voies réussies pour un utilisateur donné.
    Donne en sortie une queryset de couple (identifiant, profil / style).
    """
    filter_kwargs = {
        "user": user,
        "ouverture__bloc": bloc,
    }

    if date_seance:
        filter_kwargs["date_seance"] = date_seance
        filter_kwargs["ouverture__salle_id"] = salle_id

    successful_openings = (
        Seance.objects.filter(**filter_kwargs)
        .filter(Q(nb_top__gt=0) | Q(nb_top_lead__gt=0), ouverture__niveau__regex=niveau_pattern)
        .values_list('ouverture__id', f"ouverture__{field_name}")
        .distinct()
    )

    return calculate_distributions(successful_openings, bloc, field_name)


#######################
# Fonction principale #
#######################


def calculate_quotient_distributions(user, bloc, field_name, date_seance=None, salle_id=None):
    """
    Calcule le ratio entre les deux distributions.
    """
    global_distribution = global_user_distribution(user, bloc, field_name, salle_id)
    user_distribution = calculate_user_success_distribution(user, bloc, field_name, date_seance, salle_id)

    # Calculer les quotients tout en évitant les divisions par zéro
    return {
        key: user_distribution[key] / global_distribution[key]
        if global_distribution[key] != 0 else 0
        for key in user_distribution
    }
