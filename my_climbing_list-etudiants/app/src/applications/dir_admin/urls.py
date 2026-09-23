# applications/dir_admin/urls.py

from django.urls import path
from . import views


app_name = "dir_admin"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("participants/<int:contest_id>/", views.participants_view, name="participants"),
    path("frequentation/", views.frequentation_view, name="frequentation"),
    path("logout/", views.logout_view, name="logout"),
]
