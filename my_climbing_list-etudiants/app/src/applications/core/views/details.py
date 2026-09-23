from applications.core.decorators import non_staff_required
from django.shortcuts import render, redirect, get_object_or_404
from applications.core.models import Seance
from applications.custom_auth.models import Salle
from django.db.models import Case, When, BooleanField
from applications.core.utils import ascension_process_chart
from datetime import datetime


@non_staff_required
def details_view(request):
    """
    Vue pour afficher les détails d'une séance avec les graphiques associés.
    """
    if request.method == 'POST':
        # Stocke les données POST dans la session
        request.session['routes_order'] = request.POST.get('routes_order', '')
        request.session['salle_id'] = request.POST.get('salle_id')
        request.session['bloc'] = request.POST.get('bloc', 'false').lower() == 'true'
        
        # Spécifique au mode édition
        request.session['edit'] = True
        request.session['date_seance'] = request.POST.get('date_seance', '')

        # Redirige vers la vue confirm
        return redirect('core:confirm_session')
    
    else:
        # Récupérer les paramètres de l'URL
        date_seance = request.GET.get('date_seance')
        salle_id = request.GET.get('salle_id')
        bloc = request.GET.get('bloc') == 'True'
    
        # Obtenir les dimensions de l'écran client
        vh = request.session.get('viewport_height', 800) * 0.825
        vw = request.session.get('viewport_width', 400) * 0.825
    
        # Obtenir l'utilisateur du client
        user = request.user
    
        # Générer les graphiques de réalisation, profils et styles
        ascension_data = ascension_process_chart(
            user=user, viewport_height=vh, bloc=bloc, date_seance=date_seance, salle_id=salle_id
        )
    
        # Récupérer les ouvertures de la séance et ajouter des annotations (leaded/flashed)
        seances = (
            Seance.objects.filter(
                user=user,
                date_seance=date_seance,
                ouverture__salle_id=salle_id,
                ouverture__bloc=bloc,
            )
            .annotate(
                leaded=Case(
                    When(nb_top_lead__gt=0, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
                flashed=Case(
                    When(flash=True, then=True),
                    When(flash_lead=True, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
            )
            .order_by('id')
        )
    
        # Préparer le contexte pour le template
        context = {
            'salle_id': salle_id,
            'salle': get_object_or_404(Salle, id=salle_id),
            'bloc': bloc,
            'date_seance': datetime.strptime(date_seance, "%Y-%m-%d").date(),
            'seances': seances,
            'graph_ascension': ascension_data.get('graph_json', ''),
        }

        return render(request, 'core/details/details.html', context)
