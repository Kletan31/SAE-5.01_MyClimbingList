# applications/dir_admin/views/login.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from typing import cast


def login_view(request):
    # Déconnexion forcée des utilisateurs non superuser déjà connectés
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            logout(request)
        else:
            return redirect("dir_admin:dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user = cast(User, user)

            if user.is_superuser:
                login(request, user)
                return redirect("dir_admin:dashboard")

        # S'assure qu'aucune session n'est conservée
        logout(request)

        return render(
            request,
            "dir_admin/login/login.html",
            {"error": "Accès refusé."}
        )

    return render(request, "dir_admin/login/login.html")
