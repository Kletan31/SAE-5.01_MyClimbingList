# Simule le comportement de Nginx en production
class NoStoreCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # On applique le header uniquement aux réponses HTML
        if response.get("Content-Type", "").startswith("text/html"):
            response["Cache-Control"] = "no-store"

        return response
