# Modules
from django.shortcuts import render, get_object_or_404, redirect
from applications.core.decorators import non_staff_required
from applications.custom_auth.models import Salle
from applications.core.utils import (
    get_ouvertures_sorted,
    get_user_completed_ouvertures,
    get_recently_opened_ouvertures,
    get_project_ids_list,
)


@non_staff_required
def guidebook_view(request):
    """
    Vue pour afficher les ouvertures d'une salle sélectionnée.
    """
    if request.method == 'POST':
        # Stocke les données POST dans la session
        request.session['routes_order'] = request.POST.get('routes_order', '')
        request.session['salle_id'] = request.POST.get('salle_id')
        request.session['bloc'] = request.POST.get('bloc', 'false').lower() == 'true'
        request.session['map_display'] = request.POST.get('map_display', 'false').lower() == 'true'

        # Redirige vers la vue confirm
        return redirect('core:confirm_session')

    else:
        # Récupération des donnèes de la requête GET
        map_display = request.GET.get('map_display', 'false').lower() == 'true'
        edit = request.GET.get('edit', 'false').lower() == 'true'
        add_button = request.GET.get('add_button', 'false').lower() == 'true'
        salle_id = request.GET.get('salle_id')
        bloc = request.GET.get('bloc', 'false').lower() == 'true'

        # Récupère le nom de la salle
        salle = get_object_or_404(Salle, id=salle_id)

        # Récupère les ouvertures sous la forme de listes
        voies_ouvertures, blocs_ouvertures = get_ouvertures_sorted(salle_id)

        # Récupère les ID des ouvertures déjà réussies par l'utilisateur
        ouvertures_reussies_ids = get_user_completed_ouvertures(request.user, salle_id)

        # Récupère les ID des ouvertures récentes (moins d'une semaine)
        ouvertures_recentes_ids = get_recently_opened_ouvertures(salle_id)

        # Récupère les ID des projets de l'utilisateur
        projets_ids = get_project_ids_list(request.user, salle_id)

        return render(request, 'core/guidebook/main.html', {
            'map_display': map_display,
            'edit': edit,
            'add_button': add_button,
            'salle_id': salle_id,
            'bloc': bloc,
            'salle': salle,
            'voies_ouvertures': voies_ouvertures,
            'blocs_ouvertures': blocs_ouvertures,
            'ouvertures_reussies_ids': ouvertures_reussies_ids,
            'ouvertures_recentes_ids': ouvertures_recentes_ids,
            'projets_ids': projets_ids,
            'hide_cotation': salle.masquer_cotation_recentes,
        })
