# applications/contest/urls.py

from django.urls import path
from .views import *

app_name = "contest"

urlpatterns = [
    path("", contest_home_view, name="home"),
    path("salle/<int:salle_id>/", salle_contest_list_view, name="salle_detail"),
    path("<int:contest_id>/", contest_detail_view, name="contest_detail"),
    path("<int:contest_id>/inscription/", contest_inscription_view, name="inscription"),
    path("<int:contest_id>/resultats/", classement_topo_view, name="classement_topo"),
    path("<int:contest_id>/participant/<int:user_id>/", participant_detail_view, name="participant_detail"),
    path("<int:contest_id>/team/<int:team_id>/", team_detail_view, name="participant_detail_team"),
    path("unsubscribe/<int:contest_id>/", unsubscribe_view, name="unsubscribe"),
    path("<int:contest_id>/submit_all/", submit_contest_results_view, name="submit_contest_results"),
    path("ranking/", ranking_view, name="ranking"),
]
