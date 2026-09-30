# applications/staff_admin/views/auth.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from typing import cast


def staff_login_view(request):
    # Déconnexion forcée des utilisateurs déjà connectés mais non staff
    if request.user.is_authenticated:
        if not request.user.is_staff:
            logout(request)
        else:
            return redirect('staff_admin:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user = cast(User, user)

            if user.is_staff:
                login(request, user)
                return redirect('staff_admin:dashboard')

            # Authentifié mais non autorisé
            logout(request)
            messages.error(request, "Vous n’avez pas accès à cet espace.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")

    return render(request, 'staff_admin/auth/login.html')
