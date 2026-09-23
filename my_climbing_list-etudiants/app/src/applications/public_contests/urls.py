# applications/public_contests/urls.py

from django.urls import path
from . import views


app_name = "public_contests"

urlpatterns = [
    path("", views.contest_list_view, name="contest_list"),
    path("<int:contest_id>/", views.contest_detail_view, name="contest_detail"),
    path("ranking/", views.climber_ranking_view, name="climber_ranking"),
]
