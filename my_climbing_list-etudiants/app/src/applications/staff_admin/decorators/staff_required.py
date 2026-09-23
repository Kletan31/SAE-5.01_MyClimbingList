# applications/staff_admin/decorators/staff_required.py

from django.shortcuts import redirect
from django.contrib.auth import logout
from functools import wraps


def staff_required(view_func):
    """
    Autorise uniquement les utilisateurs staff.
    - Non connecté → redirection vers staff_admin:login
    - Connecté mais non staff → logout + redirection
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("staff_admin:login")

        if not user.is_staff:
            logout(request)
            return redirect("staff_admin:login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
