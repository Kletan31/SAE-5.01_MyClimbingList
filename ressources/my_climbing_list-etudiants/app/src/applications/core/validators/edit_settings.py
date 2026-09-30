# applications/core/validators/edit_settings.py

import re
from django.contrib.auth.models import User


def validate_email(email):
    """
    Vérifie si l'email est valide et s'il n'est pas déjà utilisé.
    :param email: L'email à valider
    :return: (bool, str) True si valide, sinon False et un message d'erreur
    """
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_regex, email):
        return False, "Format de l'email invalide"
    if User.objects.filter(email=email).exists():
        return False, "Cet email est déjà utilisé"

    return True, ""


def validate_username(username):
    """
    Vérifie si le nom d'utilisateur est valide.
    Règles :
    - 1 à 12 caractères
    - lettres minuscules, chiffres, ., _ et -
    - ne peut pas commencer ou finir par ., _ ou -
    """

    if not username:
        return False, "Le nom d'utilisateur ne peut pas être vide"

    # Uniquement minuscules, chiffres et . _ -
    username_regex = r'^[a-zA-Z0-9._-]{1,12}$'
    if not re.match(username_regex, username):
        return (
            False,
            "Le nom d’utilisateur doit contenir au maximum 12 caractères "
            "et uniquement des lettres minuscules, chiffres, points, tirets ou underscores"
        )

    # Ne pas commencer ou finir par un caractère spécial
    if username[0] in "._-" or username[-1] in "._-":
        return (
            False,
            "Le nom d’utilisateur ne peut pas commencer ou finir par un point, un tiret ou un underscore"
        )

    # Unicité
    if User.objects.filter(username=username).exists():
        return False, "Ce nom d'utilisateur est déjà utilisé"

    return True, ""


def validate_name(name):
    """
    Vérifie si un nom ou prénom est valide (texte uniquement, pas de chiffres ni de caractères spéciaux).
    :param name: Le nom ou prénom à valider
    :return: (bool, str) True si valide, sinon False et un message d'erreur
    """
    if not name.isalpha():
        return False, "Le nom ou prénom ne doit contenir que des lettres"
    return True, ""


def validate_gender(gender):
    """
    Vérifie si le genre est valide (doit être 'M' ou 'F').
    :param gender: Le genre à valider
    :return: (bool, str) True si valide, sinon False et un message d'erreur
    """
    if gender not in ['M', 'F', 'N']:
        return False, "Vous devez sélectionner un genre parmi les trois proposés pour sauvegarder"
    return True, ""
