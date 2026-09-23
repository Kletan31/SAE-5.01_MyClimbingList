from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from applications.core.utils import prepare_gym_graph
from applications.custom_auth.models import Salle


def gym_properties_refresh(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        salle_id = data.get('salle_id')  # ID de la salle envoyée depuis le frontend
        bloc = data.get('type', False)
        profil = data.get('profiles', [])
        style = data.get('styles', [])
        viewport_height = request.session.get('viewport_height', 800)  # Valeur par défaut

        salle = get_object_or_404(Salle, id=salle_id)

        # Préparer les données du graphique
        graph_json = prepare_gym_graph(salle, bloc, viewport_height, profil, style)

        return JsonResponse(graph_json)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
