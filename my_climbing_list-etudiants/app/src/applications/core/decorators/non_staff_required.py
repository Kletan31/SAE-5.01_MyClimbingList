# applications/core/decorators/non_staff_required.py

from django.shortcuts import redirect
from django.contrib.auth import logout
from functools import wraps


def non_staff_required(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect("custom_auth:login")

        if user.is_staff or user.is_superuser:
            logout(request)
            return redirect("custom_auth:login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
