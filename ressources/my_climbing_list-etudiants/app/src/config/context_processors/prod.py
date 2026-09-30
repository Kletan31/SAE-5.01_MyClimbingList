from django.conf import settings


def prod_context(request):
    return {
        'PROD': settings.PROD,
    }
