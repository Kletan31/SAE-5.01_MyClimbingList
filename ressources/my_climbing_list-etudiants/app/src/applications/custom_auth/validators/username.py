from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


# Fonction utilitaire de validation de nom d'utilisateur
def validate_custom_username(username):
    """
    Valide un nom d'utilisateur personnalisé en appliquant plusieurs règles spécifiques.

    Cette fonction utilise le validateur intégré `UnicodeUsernameValidator` pour s'assurer
    que le nom d'utilisateur respecte les caractères valides. Ensuite, elle vérifie que le
    nom d'utilisateur ne contient pas de caractère ("_") et qu'il ne dépasse pas une longueur
    maximale de douze. Si une des conditions est violée, une exception `ValidationError` est
    levée avec un message d'erreur approprié.
    """

    # Initialisation du validateur Unicode
    username_validator = UnicodeUsernameValidator()

    # Vérification du validateur Unicode
    try:
        username_validator(username)
    except ValidationError:
        raise ValidationError(_("Le nom d'utilisateur contient des caractères invalides."))

    # Vérification de la non-présence de l'underscore
    if "_" in username:
        raise ValidationError(_("Le nom d'utilisateur ne doit pas contenir de caractères de soulignement \"_\"."))

    # Vérification de la non-présence de l'arobase
    if "@" in username:
        raise ValidationError(_("Le nom d'utilisateur ne doit pas contenir de caractère \"@\"."))

    # Vérification de la longueur
    if len(username) > 12:
        raise ValidationError(_("Le nom d'utilisateur ne peut pas dépasser 12 caractères."))
