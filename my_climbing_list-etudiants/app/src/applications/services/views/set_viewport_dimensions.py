from django.http import HttpResponse
import json


def set_viewport_dimensions_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vh = data.get('vh')  # Récupérer la hauteur du viewport
            vw = data.get('vw')  # Récupérer la largeur du viewport

            if vh and vw:
                # Stocker la hauteur et la largeur dans la session Django
                request.session['viewport_height'] = vh
                request.session['viewport_width'] = vw
                return HttpResponse(status=204)
            return HttpResponse(status=400)  # Requête incorrecte si vh ou vw manquant
        except json.JSONDecodeError:
            return HttpResponse(status=400)  # Requête incorrecte si le JSON est invalide
    return HttpResponse(status=405)  # Méthode non autorisée si ce n'est pas un POST
