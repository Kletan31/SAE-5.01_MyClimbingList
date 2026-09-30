# applications/custom_auth/views/auth/login.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from typing import cast

# Messages d'erreur centralisés
login_error = "Le nom d’utilisateur ou le mot de passe ne correspondent pas."
email_error = "Cette adresse email n’est associée à aucun compte utilisateur."
staff_error = (
    "Ce compte est réservé à l’administration et ne peut pas se connecter via cette interface."
)


def login_view(request):
    """
    Gère la connexion de l'utilisateur et les erreurs de tentative.
    Gère la connexion des utilisateurs via l'adresse mail plutôt que le nom d'utilisateur.
    """

    if request.method == "GET" and request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            logout(request)
        else:
            return redirect("core:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Si l'identifiant ressemble à un email
        if "@" in username:
            try:
                username = User.objects.get(email=username).username
            except User.DoesNotExist:
                return render(request, "custom_auth/auth/login.html", {
                    "error": True,
                    "error_message": email_error,
                    "page_to_load": "login",
                })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user = cast(User, user)

            if user.is_staff or user.is_superuser:
                logout(request)
                return render(request, "custom_auth/auth/login.html", {
                    "error": True,
                    "error_message": staff_error,
                    "page_to_load": "login",
                })

            login(request, user)
            return redirect("core:home")

        return render(request, "custom_auth/auth/login.html", {
            "error": True,
            "error_message": login_error,
            "page_to_load": "login",
        })

    return render(request, "custom_auth/auth/login.html")
