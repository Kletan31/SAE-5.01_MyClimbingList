# applications/core/views/salle_list.py
from django.shortcuts import render, redirect
from applications.core.decorators import non_staff_required
from applications.core.utils import get_salle_progress, find_max_salles, clear_specific_session_data


@non_staff_required
def salle_list_view(request):
    user = request.user
    force_list = request.GET.get("force_list")

    # Redirection automatique si favori et pas de "force_list"
    favorite = getattr(getattr(user, "profile", None), "favorite_salle", None)
    if favorite and not force_list:
        return redirect(f"{request.build_absolute_uri('/core/guidebook/')}?salle_id={favorite.id}&map_display=True")

    # Affichage normal de la liste
    salles_progress = get_salle_progress(user)
    keys_to_clear = ['routes_order', 'salle_id', 'bloc', 'edit', 'date_seance']
    clear_specific_session_data(request, keys_to_clear)

    return render(request, 'core/salle_list/salle_list.html', {
        'salles': salles_progress,
        'preferred_gym': find_max_salles(salles_progress),
    })
