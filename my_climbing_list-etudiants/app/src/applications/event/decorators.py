from functools import wraps
from urllib.parse import urlencode

from django.contrib.auth import logout
from django.shortcuts import redirect


def event_staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        login_url = "event:staff_login"

        next_url = request.get_full_path()
        query_string = urlencode({"next": next_url})

        if not user.is_authenticated:
            return redirect(f"{redirect(login_url).url}?{query_string}")

        if not user.is_staff:
            logout(request)
            return redirect(f"{redirect(login_url).url}?{query_string}")

        return view_func(request, *args, **kwargs)

    return _wrapped_view