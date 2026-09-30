# applications/staff_admin/views/logout.py

from django.contrib.auth import logout
from django.shortcuts import redirect


def staff_logout_view(request):
    logout(request)
    return redirect("staff_admin:login")
