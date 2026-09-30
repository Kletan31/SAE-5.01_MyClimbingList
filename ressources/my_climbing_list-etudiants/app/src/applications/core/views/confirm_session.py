from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from applications.core.decorators import non_staff_required
from applications.custom_auth.models import Salle

from applications.core.utils import (
    parse_routes_order,
    get_routes_with_details_optimized,
    sort_routes_by_order,
    save_session_data,
    edit_session_data,
    get_recently_opened_ouvertures
)


@non_staff_required
def confirm_session_view(request):
    if request.method == 'POST':
        return process_post_request(request)
    else:
        return render_confirm_page(request)


def render_confirm_page(request):
    edit = request.session.get('edit', False)
    map_display = request.session.get('map_display', True)
    routes_order_str = request.session.get('routes_order', '')
    original_date_seance = request.session.get('date_seance', '')
    salle_id = request.session.get('salle_id', None)
    bloc = request.session.get('bloc', False)
    add_button = True if routes_order_str else False
    routes_order = parse_routes_order(routes_order_str)

    routes, already_try = get_routes_with_details_optimized(routes_order, request.user, salle_id)
    routes = sort_routes_by_order(routes, routes_order)

    salle = Salle.objects.get(id=salle_id) if salle_id else None
    hide_cotation = salle.masquer_cotation_recentes if salle else False
    ouvertures_recentes_ids = get_recently_opened_ouvertures(salle_id) if hide_cotation else []

    return render(request, 'core/confirm_session/confirm_session.html', {
        'map_display': map_display,
        'edit': edit,
        'date_seance': original_date_seance,
        'routes': routes,
        'already_try': already_try,
        'salle_id': salle_id,
        'bloc': bloc,
        'add_button': add_button,
        'routes_order': routes_order_str,
        'today': date.today().isoformat(),
        'hide_cotation': hide_cotation,
        'ouvertures_recentes_ids': ouvertures_recentes_ids,
    })


def process_post_request(request):
    if request.session.get('edit', False):
        original_date_seance = request.session.get('date_seance')
        salle_id = request.session.get('salle_id')
        bloc = request.session.get('bloc')

        redirect_home, new_date_seance = edit_session_data(request.user, request.POST, original_date_seance, salle_id, bloc)

        if redirect_home:
            return redirect('core:home')

        return redirect(f'{reverse("core:details")}?date_seance={new_date_seance}&salle_id={salle_id}&bloc={bloc}')
    else:
        save_session_data(request.user, request.POST)
        return redirect('core:home')
