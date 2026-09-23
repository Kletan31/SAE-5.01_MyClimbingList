from django.http import FileResponse, Http404
from django.contrib.staticfiles import finders


def custom_static_serve(request, path):
    """Servir les fichiers statiques avec des en-têtes personnalisés."""
    # Recherche le fichier dans tous les répertoires `static`
    resolved_path = finders.find(path)

    if not resolved_path:
        raise Http404(f"Static file not found: {path}")

    # Crée une réponse pour le fichier et ajoute un en-tête de cache personnalisé
    response = FileResponse(open(resolved_path, 'rb'))
    response["Cache-Control"] = "public, max-age=604800, immutable"
    return response
