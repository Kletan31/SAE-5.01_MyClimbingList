# applications/dir_admin/decorators/superuser_required.py

from django.shortcuts import redirect
from django.contrib.auth import logout
from functools import wraps


def superuser_required(view_func):
    """
    Autorise uniquement les superusers.
    - Non connecté → redirection vers dir_admin:login
    - Connecté mais non superuser → logout + redirection
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("dir_admin:login")

        if not user.is_superuser:
            logout(request)
            return redirect("dir_admin:login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
