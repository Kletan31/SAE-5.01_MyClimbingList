# applications/custom_auth/views/auth/register.py

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from applications.custom_auth.models import Profile
from applications.core.validators import validate_email, validate_username


# Messages d'erreur centralisés
pwd_error = "Les mots de passe ne correspondent pas."


def register_view(request):
    """Gère l'inscription d'un nouvel utilisateur avec validation des informations."""

    # Déconnexion forcée des comptes staff / superuser pour éviter les boucles
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            logout(request)
        else:
            return redirect('core:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        try:
            # -----------------------------
            # Validation username
            # -----------------------------
            is_valid, error_message = validate_username(username)
            if not is_valid:
                raise ValidationError(error_message)

            # -----------------------------
            # Validation email
            # -----------------------------
            is_valid, error_message = validate_email(email)
            if not is_valid:
                raise ValidationError(error_message)

            # -----------------------------
            # Validation mots de passe
            # -----------------------------
            if password1 != password2:
                raise ValidationError(pwd_error)

            validate_password(password1)

            # -----------------------------
            # Création utilisateur + profil
            # -----------------------------
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                )
                Profile.objects.create(user=user)

            # Connexion automatique
            login(request, user)
            return redirect('core:home')

        except ValidationError as e:
            return render(
                request,
                'custom_auth/auth/register.html',
                context={
                    'error': True,
                    'error_message': e.messages[0],
                    'page_to_load': 'register',
                }
            )

    return render(request, 'custom_auth/auth/register.html')
