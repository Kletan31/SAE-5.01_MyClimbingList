from django.http import HttpResponse
from django.conf import settings


def service_worker_view(request):
    """
    Vue pour servir le fichier service-worker.js avec les valeurs DEBUG et APP_VERSION injectées dynamiquement.
    """
    service_worker_path = 'static/base/pwa/config/sw/sw.js'

    with open(service_worker_path, 'r', encoding='utf-8') as file:
        service_worker_script = file.read()

    # Injecter la valeur de settings.PROD dans le script
    log_value = 'false' if settings.PROD else 'true'
    service_worker_script = service_worker_script.replace(
        'let LOG = false;',
        f'let LOG = {log_value};'
    )

    # Injecter la valeur de settings.APP_VERSION dans le script
    service_worker_script = service_worker_script.replace(
        "const CACHE_VERSION = '';",
        f"const CACHE_VERSION = '{settings.APP_VERSION}';"
    )

    # Crée une réponse pour le fichier et ajoute un en-tête de cache personnalisé
    response = HttpResponse(service_worker_script, content_type='application/javascript')
    response['Cache-Control'] = 'public, max-age=31536000, immutable'
    return response
