import json
from django.http import JsonResponse
from django.conf import settings


def manifest_view(request):
    """
    Vue pour servir le fichier manifest.json modifié dynamiquement.
    """
    # Chemin vers le fichier manifest.json statique
    manifest_path = 'static/base/pwa/config/manifest/manifest.json'

    # Charger les données JSON du fichier manifest.json
    with open(manifest_path, 'r', encoding='utf-8') as file:
        manifest_data = json.load(file)

    # Dynamiser "start_url" en fonction de PROD
    if settings.PROD:
        manifest_data["start_url"] = "/"
    else:
        # Utiliser l'URL de production par défaut
        manifest_data["start_url"] = "https://localhost:8000/"

    # Retourner le manifest JSON modifié
    return JsonResponse(manifest_data)
