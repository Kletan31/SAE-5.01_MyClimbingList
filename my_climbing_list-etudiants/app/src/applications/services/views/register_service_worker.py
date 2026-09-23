from django.http import HttpResponse
from django.conf import settings


def register_service_worker_view(request):
    """
    Vue pour servir le fichier register_service-worker.js avec une valeur APP_VERSION injectée dynamiquement.
    """
    # Récupérer le script initial
    register_register_service_worker_path = 'static/base/js/init/registerServiceWorker.js'

    # Injecter la valeur de settings.APP_VERSION dans le script
    with open(register_register_service_worker_path, 'r', encoding='utf-8') as file:
        register_service_worker_script = file.read()

    register_service_worker_script = register_service_worker_script.replace(
        "const SW_VERSION = '';",
        f"const SW_VERSION = '{settings.APP_VERSION}';"
    )

    # Retourner le script modifié
    return HttpResponse(register_service_worker_script, content_type='application/javascript')
