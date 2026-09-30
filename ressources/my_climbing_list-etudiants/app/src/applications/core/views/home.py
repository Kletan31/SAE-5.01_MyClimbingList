from django.shortcuts import render
from applications.core.decorators import non_staff_required
from applications.core.utils import (
    get_user_seances,
    aggregate_seances_data,
    get_weekly_stats,
    count_total_user_sessions,
    clear_specific_session_data,
    popup_info,
)


@non_staff_required
def home_view(request):
    user = request.user
    popup_to_show = popup_info(user)

    seances = get_user_seances(user)
    seances_data = aggregate_seances_data(seances, limit=20)
    weekly_stats = get_weekly_stats(user)
    total_seances = count_total_user_sessions(user)

    keys_to_clear = ['routes_order', 'salle_id', 'bloc', 'edit', 'date_seance', 'map_display']
    clear_specific_session_data(request, keys_to_clear)

    return render(request, 'core/home/home.html', {
        'popup_to_show': popup_to_show,
        'seances_data': seances_data,
        'weekly_stats': weekly_stats,
        'total_seances': total_seances,
    })
