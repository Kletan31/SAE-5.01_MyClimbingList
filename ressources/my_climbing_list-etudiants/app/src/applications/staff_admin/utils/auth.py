# applications/core/utils/auth.py

from django.core.exceptions import PermissionDenied


def get_salle_from_request(request):
    """
    Retourne la salle associée à l'utilisateur connecté.

    - nécessite un utilisateur authentifié
    - nécessite un profile
    - nécessite une salle associée
    """

    user = request.user

    if not user.is_authenticated:
        raise PermissionDenied("Utilisateur non authentifié")

    if not hasattr(user, "profile"):
        raise PermissionDenied("Aucun profil associé à cet utilisateur")

    if not user.profile.salle_voie:
        raise PermissionDenied("Aucune salle associée à ce compte")

    return user.profile.salle_voie
