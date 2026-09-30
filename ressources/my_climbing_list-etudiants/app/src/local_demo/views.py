"""Adaptations locales des ressources PWA existantes, sans URL distante."""
import json

from django.http import HttpResponse, JsonResponse
from applications.services.views.manifest import manifest_view
from applications.services.views.service_worker import service_worker_view


def manifest(request):
    data = json.loads(manifest_view(request).content)
    data.update(name="My Climbing List — Local", short_name="MCL Local",
                start_url="/", scope="/", id="/")
    response = JsonResponse(data)
    response["Cache-Control"] = "no-store"
    return response


def service_worker(request):
    response = service_worker_view(request)
    # Le cache applicatif historique ne doit pas figer le manifest ni le script
    # d'enregistrement pendant les exercices locaux.
    script = response.content.decode().replace(
        "const requestUrl = new URL(event.request.url);",
        """const requestUrl = new URL(event.request.url);
    if (requestUrl.origin !== self.location.origin ||
        ['/manifest.json', '/register-service-worker.js', '/service-worker.js']
            .includes(requestUrl.pathname)) return;""",
        1,
    )
    response.content = script
    response["Cache-Control"] = "no-store"
    return response


def register_service_worker(request):
    # Le navigateur vérifie les modifications à chaque visite, sans placeholder
    # ni version mémorisée qui masquerait les changements faits par les étudiants.
    script = """if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js', {
            scope: '/', updateViaCache: 'none'
        }).catch(error => console.error('Service worker local :', error));
    }"""
    response = HttpResponse(script, content_type="application/javascript")
    response["Cache-Control"] = "no-store"
    return response
