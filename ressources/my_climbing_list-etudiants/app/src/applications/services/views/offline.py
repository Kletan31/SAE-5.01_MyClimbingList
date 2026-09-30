from django.shortcuts import render


def offline_view(request):
    """Affiche la page hors ligne."""
    return render(request, 'services/offline/offline.html')
