from django.shortcuts import redirect


def csrf_failure_view(request, reason=""):
    return redirect('custom_auth:login')
