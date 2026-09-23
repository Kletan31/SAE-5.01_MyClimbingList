# applications/dir_admin/views/logout.py

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    logout(request)
    return redirect("dir_admin:login")
