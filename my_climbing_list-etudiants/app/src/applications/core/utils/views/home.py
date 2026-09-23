from django.db.models import Q, Sum, Max, F, Count
from applications.core.models import Seance
from datetime import datetime, timedelta
from applications.core.utils import cotation_colors
from applications.core.models import MessagePopup, MessagePopupView
from django.utils.translation import get_language


def get_user_seances(user):
    """
    Récupère les séances de l'utilisateur en excluant celles sans ascension ni échec.
    :param user: Objet User de Django représentant l'utilisateur connecté.
    :return: QuerySet de séances filtrées et ordonnées.
    """
    return (
        Seance.objects.filter(user=user)
        .select_related('ouverture', 'ouverture__salle')
        .exclude(Q(nb_top=0) & Q(nb_try=0) & Q(nb_top_lead=0) & Q(nb_try_lead=0))
        .order_by('-date_seance', '-id')
    )


def aggregate_seances_data(seances, offset=0, limit=10):
    """
    Agrège les données pour les séances paginées.
    Une séance est définie par la combinaison (salle, date, bloc).
    """
    from django.db.models import Sum, Max, F, Q

    # Étape 1 : identifier les combinaisons uniques triées
    sessions = (
        seances
        .values('ouverture__salle__id', 'ouverture__bloc', 'date_seance')
        .distinct()
        .order_by('-date_seance', '-ouverture__salle__id', '-ouverture__bloc')
    )[offset:offset + limit]

    # Étape 2 : extraire les tuples distincts
    session_filters = [
        (s['ouverture__salle__id'], s['date_seance'], s['ouverture__bloc'])
        for s in sessions
    ]

    if not session_filters:
        return {}

    # Étape 3 : construire le filtre combiné
    query = Q()
    for salle_id, date_seance, bloc in session_filters:
        query |= Q(
            ouverture__salle__id=salle_id,
            date_seance=date_seance,
            ouverture__bloc=bloc,
        )

    # Étape 4 : regrouper et agréger
    aggregated = (
        seances.filter(query)
        .values(
            'ouverture__salle__nom',
            'ouverture__salle__id',
            'ouverture__bloc',
            'date_seance',
        )
        .annotate(
            total_try=Sum(F('nb_try') + F('nb_try_lead')),
            total_top=Sum(F('nb_top') + F('nb_top_lead')),
            max_cotation=Max('ouverture__niveau'),
        )
        .order_by('-date_seance', '-ouverture__salle__id')
    )

    # Étape 5 : formatage final
    seances_data = {}
    for row in aggregated:
        salle_nom = row['ouverture__salle__nom']
        salle_id = row['ouverture__salle__id']
        bloc = row['ouverture__bloc']
        date_seance = row['date_seance']
        max_cotation = row['max_cotation'] or '-'

        cotation_color = (
            cotation_colors.get(max_cotation[0], '#000')
            if max_cotation != '-' else '#000'
        )

        key = (salle_nom, date_seance, salle_id, bloc)
        seances_data[key] = {
            'total_try': row['total_try'] or 0,
            'total_top': row['total_top'] or 0,
            'max_cotation': max_cotation,
            'cotation_color': cotation_color,
        }

    return seances_data


def get_weekly_stats(user):
    """
    Retourne les statistiques de la semaine en cours.
    Une séance est définie par le triplet (salle, date, bloc).
    """

    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)

    # Base filtrée semaine + séances non vides
    base_qs = (
        Seance.objects
        .filter(
            user=user,
            date_seance__gte=start_of_week.date(),
            date_seance__lt=end_of_week.date(),
        )
        .exclude(Q(nb_top=0) & Q(nb_try=0) & Q(nb_top_lead=0) & Q(nb_try_lead=0))
    )

    # --- Comptage des séances LOGIQUES ---
    session_base = (
        base_qs
        .values(
            'ouverture__salle_id',
            'date_seance',
            'ouverture__bloc',
        )
        .distinct()
    )

    session_counts = session_base.aggregate(
        bloc=Count('date_seance', filter=Q(ouverture__bloc=True)),
        voie=Count('date_seance', filter=Q(ouverture__bloc=False)),
    )

    # --- Agrégations classiques ---
    stats = (
        base_qs
        .values('ouverture__bloc')
        .annotate(
            total_try=Sum(F('nb_try') + F('nb_try_lead')),
            total_top=Sum(F('nb_top') + F('nb_top_lead')),
            max_cotation=Max('ouverture__niveau'),
        )
    )

    # Initialisation
    weekly_stats = {
        'nombre_seances_bloc': session_counts['bloc'] or 0,
        'nombre_seances_voie': session_counts['voie'] or 0,
        'total_try_bloc': 0,
        'total_top_bloc': 0,
        'total_try_voie': 0,
        'total_top_voie': 0,
        'cotation_max_bloc': '-',
        'cotation_max_voie': '-',
    }

    # Répartition bloc / voie
    for s in stats:
        bloc = s['ouverture__bloc']
        if bloc:
            weekly_stats['total_try_bloc'] = s['total_try'] or 0
            weekly_stats['total_top_bloc'] = s['total_top'] or 0
            weekly_stats['cotation_max_bloc'] = s['max_cotation'] or '-'
        else:
            weekly_stats['total_try_voie'] = s['total_try'] or 0
            weekly_stats['total_top_voie'] = s['total_top'] or 0
            weekly_stats['cotation_max_voie'] = s['max_cotation'] or '-'

    return weekly_stats


def clear_specific_session_data(request, keys_to_clear):
    """
    Supprime des clés spécifiques de la session utilisateur.
    :param request: Objet HttpRequest
    :param keys_to_clear: Liste des clés à supprimer de la session.
    """
    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]


def popup_info(user):
    """
    Renvoie la traduction du dernier message à afficher pour l'utilisateur.
    """
    if not user.is_authenticated:
        return None

    # Récupère le dernier message créé
    popup = MessagePopup.objects.order_by('-created_at').first()
    if not popup:
        return None

    # Vérifie si l'utilisateur l'a déjà vu
    already_seen = MessagePopupView.objects.filter(user=user, popup=popup).exists()
    if already_seen:
        return None

    # Récupère la traduction dans la langue active
    lang = get_language() or 'fr'
    translation = popup.translations.filter(language=lang).first()

    # Fallback si la traduction n'existe pas
    if not translation:
        translation = popup.translations.filter(language='en').first() or popup.translations.first()

    # On renvoie un petit dictionnaire pratique pour le template
    return {
        'id': popup.id,
        'code': popup.code,
        'title': translation.title if translation else '',
        'content': translation.content if translation else '',
    }


def count_total_user_sessions(user):
    """
    Nombre total de séances distinctes (triplet: salle, date, bloc) pour un utilisateur,
    avec séparation bloc/voie.
    """
    from applications.core.models import Seance

    base = (
        Seance.objects
        .filter(user=user)
        .exclude(Q(nb_top=0) & Q(nb_try=0) & Q(nb_top_lead=0) & Q(nb_try_lead=0))
        .values('ouverture__salle_id', 'date_seance', 'ouverture__bloc')  # triplet logique
        .distinct()
    )

    agg = base.aggregate(
        total=Count('date_seance'),
        voie=Count('date_seance', filter=Q(ouverture__bloc=False)),
        bloc=Count('date_seance', filter=Q(ouverture__bloc=True)),
    )

    return {
        'bloc': agg['bloc'] or 0,
        'voie': agg['voie'] or 0,
        'total': agg['total'] or 0,
    }
