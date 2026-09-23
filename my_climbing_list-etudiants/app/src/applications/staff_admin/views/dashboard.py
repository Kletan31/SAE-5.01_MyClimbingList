# applications/staff_admin/views/dashboard.py

from django.shortcuts import render
from applications.staff_admin.decorators import staff_required


@staff_required
def dashboard_view(request):
    return render(
        request,
        "staff_admin/dashboard/dashboard.html",
        {
            "is_dashboard": True,
        }
    )
