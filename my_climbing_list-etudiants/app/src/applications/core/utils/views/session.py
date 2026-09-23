from django.shortcuts import get_object_or_404
from applications.core.models import Ouverture, Seance, Salle
from django.db.models import Sum
from datetime import date
from django.db import transaction


def parse_routes_order(routes_order_str):
    if not routes_order_str:
        return []
    return [int(route_id) for route_id in routes_order_str.split(',') if route_id.isdigit()]


def get_routes_with_details_optimized(routes_ids, user, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    relais_en_tete = salle.relais_en_tete
    routes = Ouverture.objects.filter(id__in=routes_ids).select_related('salle')

    past_sessions = Seance.objects.filter(user=user, ouverture__in=routes).values(
        'ouverture_id'
    ).annotate(
        total_top=Sum('nb_top'),
        total_try=Sum('nb_try'),
        total_top_lead=Sum('nb_top_lead'),
        total_try_lead=Sum('nb_try_lead')
    )
    past_data_map = {session['ouverture_id']: session for session in past_sessions}
    already_try_ids = set(past_data_map.keys())

    for route in routes:
        route.leadable = not route.bloc and (route.relais in relais_en_tete)
        data = past_data_map.get(route.id)
        if data:
            route.past_top = data['total_top'] or 0
            route.past_try = data['total_try'] or 0
            route.past_top_lead = data['total_top_lead'] or 0
            route.past_try_lead = data['total_try_lead'] or 0
        else:
            route.past_top = 0
            route.past_try = 0
            route.past_top_lead = 0
            route.past_try_lead = 0

    return routes, already_try_ids


def sort_routes_by_order(routes, route_ids_order):
    id_to_position = {route_id: index for index, route_id in enumerate(route_ids_order)}
    return sorted(routes, key=lambda route: id_to_position.get(route.id, float('inf')))


def parse_session_data(post_data):
    date_seance = post_data.get('date_seance', date.today().isoformat())
    routes_order_str = post_data.get('routes_order', '')
    routes_order = parse_routes_order(routes_order_str)
    return date_seance, routes_order


def save_or_update_session(user, route_id, date_seance, post_data):
    nb_try = int(post_data.get(f'nb_try_{route_id}', 0))
    nb_top = int(post_data.get(f'nb_top_{route_id}', 0))
    flash = post_data.get(f'flash_{route_id}', 'false').lower() == 'true'

    nb_try_lead = int(post_data.get(f'nb_try_{route_id}_lead', 0))
    nb_top_lead = int(post_data.get(f'nb_top_{route_id}_lead', 0))
    flash_lead = post_data.get(f'flash_{route_id}_lead', 'false').lower() == 'true'

    flash_available = post_data.get(f'flash_available_{route_id}', 'true').lower() == 'true'

    if nb_try == 0 and nb_top == 0 and nb_try_lead == 0 and nb_top_lead == 0:
        return False

    Seance.objects.update_or_create(
        user=user,
        ouverture_id=route_id,
        date_seance=date_seance,
        defaults={
            'nb_top': nb_top,
            'nb_try': nb_try,
            'flash': flash,
            'nb_top_lead': nb_top_lead,
            'nb_try_lead': nb_try_lead,
            'flash_lead': flash_lead,
            'flash_available': flash_available,
        }
    )
    return True


def save_session_data(user, post_data):
    date_seance, routes_order = parse_session_data(post_data)
    for route_id in routes_order:
        save_or_update_session(user, route_id, date_seance, post_data)


def edit_session_data(user, post_data, original_date_seance, salle_id, bloc):
    # Séances présentes à l’ANCIENNE date (scopées salle/bloc)
    existing_sessions = Seance.objects.filter(
        user=user,
        date_seance=original_date_seance,
        ouverture__bloc=bloc,
        ouverture__salle_id=salle_id,
    )
    existing_route_ids = set(existing_sessions.values_list('ouverture_id', flat=True))

    # Données du formulaire
    new_date_seance, routes_order = parse_session_data(post_data)
    requested_route_ids = {int(rid) for rid in routes_order}

    # Voies à déplacer = celles qui existaient à l’ancienne date ET sont encore demandées
    to_move_ids = existing_route_ids & requested_route_ids
    # Voies obsolètes = présentes avant mais plus demandées
    obsolete_route_ids = existing_route_ids - requested_route_ids

    updated_route_ids = set()

    with transaction.atomic():
        # 1) Si la date change, on purge d’abord d’éventuels doublons déjà à la NOUVELLE date
        if original_date_seance != new_date_seance and to_move_ids:
            Seance.objects.filter(
                user=user,
                date_seance=new_date_seance,
                ouverture__bloc=bloc,
                ouverture__salle_id=salle_id,
                ouverture_id__in=to_move_ids,
            ).delete()

        # 2) On crée/met à jour à la NOUVELLE date via la fonction existante
        for route_id in routes_order:
            if save_or_update_session(user, route_id, new_date_seance, post_data):
                updated_route_ids.add(int(route_id))

        # 3) Supprimer les obsolètes à l’ANCIENNE date
        if obsolete_route_ids:
            Seance.objects.filter(
                user=user,
                date_seance=original_date_seance,
                ouverture__bloc=bloc,
                ouverture__salle_id=salle_id,
                ouverture_id__in=obsolete_route_ids
            ).delete()

        # 4) Si la date a changé, supprimer les anciennes lignes (à l’ANCIENNE date)
        #    pour les voies effectivement mises à jour
        if original_date_seance != new_date_seance and updated_route_ids:
            Seance.objects.filter(
                user=user,
                date_seance=original_date_seance,
                ouverture__bloc=bloc,
                ouverture__salle_id=salle_id,
                ouverture_id__in=updated_route_ids
            ).delete()

    # Même logique de retour que ta version
    redirect_home = (obsolete_route_ids == existing_route_ids) and (len(updated_route_ids) == 0)
    return redirect_home, new_date_seance
