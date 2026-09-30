from django.conf import settings


def local_context(request):
    return {"MCL_LOCAL": True, "PWA_ENABLED": settings.PWA_ENABLED}
