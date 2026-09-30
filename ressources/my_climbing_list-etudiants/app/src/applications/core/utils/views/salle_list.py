# applications/core/utils/views/salle_list.py

# Modules
from applications.core.models import Ouverture, Seance
from applications.custom_auth.models import Salle
from django.db.models import Q, Sum

# REGEX pour exclure les voies "découvertes" (3, 3+, 4, et 4+ inclus)
niveau_pattern = r'^[5-9]'


def get_total_ouvertures(salle_id, bloc):
    """
    Récupérer le nombre total d'ouvertures pour un type donné (bloc/voie) et une salle donnée.
    """
    return Ouverture.objects.filter(
        salle=salle_id,
        bloc=bloc,
        active=True,
        niveau__regex=niveau_pattern
    ).count()


def get_user_ouvertures(user, salle_id, bloc):
    """
    Récupérer le nombre de tops réalisés par l'utilisateur pour un type donné (bloc/voie) et une salle donnée.
    """
    return Seance.objects.filter(
        Q(nb_top__gt=0) | Q(nb_top_lead__gt=0),
        user=user,
        ouverture__salle=salle_id,
        ouverture__bloc=bloc,
        ouverture__active=True,
        ouverture__niveau__regex=niveau_pattern
    ).order_by('ouverture').distinct('ouverture').count()


def get_user_total_try(user, salle_id, bloc):
    """
    Récupérer la somme totale des montées (nb_try et nb_try_lead) pour un utilisateur et une salle donnée.
    """
    # Construire le filtre de base
    filters = {
        'user': user,
        'ouverture__salle': salle_id,
        'ouverture__active': True,
        'ouverture__niveau__regex': niveau_pattern
    }

    # Ajouter la condition sur le bloc si elle est fournie
    if bloc is not None:
        filters['ouverture__bloc'] = bloc

    # Exécuter la requête avec les filtres définis
    total_nb_try = Seance.objects.filter(**filters).aggregate(
        total_try=Sum('nb_try'),
        total_try_lead=Sum('nb_try_lead')
    )

    total_combined_try = (total_nb_try.get('total_try') or 0) + (total_nb_try.get('total_try_lead') or 0)

    return total_combined_try


def calculate_progression(user_count, total_count):
    """
    Calculer la progression en pourcentage.
    """
    progression = (user_count / total_count) * 100 if total_count > 0 else 0
    progression = min(progression, 100)
    return int(progression)


def get_salle_progress(user):
    """
    Récupérer la progression des utilisateurs pour chaque salle (blocs et voies).
    """
    salles = Salle.objects.all()
    salles_progress = []

    for salle in salles:
        total_blocs = get_total_ouvertures(salle.id, bloc=True)
        total_user_bloc_top = get_user_ouvertures(user, salle.id, bloc=True)
        progression_bloc = calculate_progression(total_user_bloc_top, total_blocs)

        total_voies = get_total_ouvertures(salle.id, bloc=False)
        total_user_voie_top = get_user_ouvertures(user, salle.id, bloc=False)
        progression_voie = calculate_progression(total_user_voie_top, total_voies)

        total_user_try = get_user_total_try(user, salle.id, bloc=None)  # Paramètre de tri dans la vue core:list

        # Paramètre pour déterminer la salle préférée (Bloc/Voie)
        total_user_bloc_try = get_user_total_try(user, salle.id, bloc=True)
        total_user_voie_try = get_user_total_try(user, salle.id, bloc=False)

        salles_progress.append((
            salle.id,
            salle.nom,
            progression_bloc,
            progression_voie,
            f'core/media/salles/{salle.id}.jpg',
            total_blocs,
            total_voies,
            total_user_try,
            total_user_bloc_try,
            total_user_voie_try,
        ))

    salles_progress.sort(key=lambda x: x[7], reverse=True)

    return salles_progress


def find_max_salles(salles_progress):
    """
    Trouve les noms des salles préférées pour la voie et le bloc.

    :param salles_progress: Liste de tuples au format (id, salle, voie_progress, bloc_progress, chemin_image).
    :return: Dictionnaire avec les noms des salles ayant les plus grands voie_progress et bloc_progress.
    """

    if not salles_progress:
        return {'voie': None, 'bloc': None}

    # Trouver le tuple avec l'élément 2 le plus grand [bloc]
    max_bloc_tuple = max(salles_progress, key=lambda x: x[8])
    max_bloc_salle = max_bloc_tuple[1] if max_bloc_tuple[8] > 0 else '-'

    # Trouver le tuple avec l'élément 3 le plus grand [voie]
    max_voie_tuple = max(salles_progress, key=lambda x: x[9])
    max_voie_salle = max_voie_tuple[1] if max_voie_tuple[9] > 0 else '-'

    return {
        'voie': max_voie_salle,
        'bloc': max_bloc_salle
    }
