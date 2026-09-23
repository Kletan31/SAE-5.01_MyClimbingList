from django.shortcuts import render


def offline_view(request):
    """Vue qui sert le template de connexion perdue."""
    return render(request, 'core/offline/offline.html')
