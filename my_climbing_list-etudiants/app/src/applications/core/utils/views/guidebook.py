# Modules
from django.db.models import Q
from applications.core.models import Ouverture, Seance
from datetime import timedelta
from django.utils import timezone
from applications.core.utils.views.projects import get_user_projects


def get_ouvertures_sorted(salle_id):
    """
    Récupère les ouvertures en appliquant systématiquement un tri sur les relais en ordre croissant.
    """

    voies_ouvertures = Ouverture.objects.filter(
        active=True, salle=salle_id, bloc=False
    ).order_by("relais", "niveau")

    blocs_ouvertures = Ouverture.objects.filter(
        active=True, salle=salle_id, bloc=True
    ).order_by("relais", "niveau")

    return voies_ouvertures, blocs_ouvertures


def get_user_completed_ouvertures(user, salle_id):
    """
    Récupère les ID des voies que l'utilisateur a déjà réussies.
    """
    return set(Seance.objects.filter(
        Q(nb_top__gt=0) | Q(nb_top_lead__gt=0),
        user=user,
        ouverture__salle=salle_id
    ).values_list('ouverture_id', flat=True))


def get_recently_opened_ouvertures(salle_id, bloc=None):
    """
    Récupère les ID des voies ouvertes il y a moins d'une semaine,
    avec un filtre optionnel pour le type de voie (bloc ou non).

    :param salle_id: Identifiant de la salle
    :param bloc: Boolean pour filtrer par type de voie (True pour bloc, False pour voie).
                 Si None, ne filtre pas selon le type.
    :return: Queryset des IDs des voies ouvertes récemment
    """
    one_week_ago = timezone.now().date() - timedelta(days=7)

    # Filtre de base
    filters = {
        'active': True,
        'salle': salle_id,
        'date_ouverture__gte': one_week_ago
    }

    # Ajouter le filtre 'bloc' seulement s'il est spécifié
    if bloc is not None:
        filters['bloc'] = bloc

    # Appliquer les filtres et retourner les IDs des voies récentes
    return set(Ouverture.objects.filter(**filters).values_list('id', flat=True))


def get_project_ids_list(user, salle_id):
    """
    Convertit la liste des projets en une liste d'ID des ouvertures.

    :param user: Utilisateur
    :param salle_id: Identifiant de la salle
    :return: Liste des ID d'ouvertures des projets
    """
    projects = get_user_projects(user)

    # Filtrer par salle
    filtered_projects = [p for p in projects if p['salle'].id == int(salle_id)]

    return [p['ouverture_id'] for p in filtered_projects]
