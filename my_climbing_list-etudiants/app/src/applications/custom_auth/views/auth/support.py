from django.shortcuts import render, redirect
from django.contrib.auth import logout


def support_view(request):
    """Affiche la page de support."""

    # Déconnexion forcée des comptes staff / superuser pour éviter les boucles
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            logout(request)
        else:
            return redirect('core:home')

    return render(request, 'custom_auth/auth/support.html')
