# applications/staff_admin/middleware/staff_required.py

from django.shortcuts import redirect
from django.urls import reverse, resolve


class StaffAccessMiddleware:
    """
    - Si l'URL commence par /staff/ :
        * Non connecté ou non staff → redirige vers /staff/login/?next=...
        * Si la vue n'existe pas → staff connecté redirigé vers /staff/dashboard/
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith("/staff/") and path not in ("/staff/login", "/staff/login/"):
            # 1) L'utilisateur doit être staff
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect(reverse("staff_admin:login"))

            # 2) Résolution d'URL
            match = resolve(path)
            if match.app_name != "staff_admin":  # Sortie de l'espace staff
                return redirect(reverse("staff_admin:dashboard"))

        return self.get_response(request)
