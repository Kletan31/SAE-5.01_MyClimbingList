# applications/staff_admin/urls.py

from django.urls import path
from .views import *

app_name = "staff_admin"

urlpatterns = [
    path("login/", staff_login_view, name="login"),
    path("logout/", staff_logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("creer/", create_contest_view, name="create_contest"),
    path("contests/", contest_list_view, name="contest_list"),
    path("contests/<int:pk>/edit/", edit_contest_view, name="edit_contest"),
    path("contests/<int:pk>/delete/", delete_contest_view, name="delete_contest"),
    path("contests/<int:contest_id>/inscriptions/", inscriptions_view, name="inscriptions"),
    path("permanents/", toggle_permanent_contests_view, name="toggle_permanents"),
    path("contest/<int:contest_id>/ouvertures/", contest_ouverture_detail_view, name="contest_ouvertures"),
    path("contest/<int:contest_id>/ouverture/<int:ouverture_id>/reussites/", ouverture_success_view, name="ouverture_success"),
    path("contests/<int:contest_id>/export/csv/", export_classement_csv_view, name="export_classement_csv"),
    path("contests/<int:contest_id>/export/pdf/", export_classement_pdf_view, name="export_classement_pdf"),
    path("contests/<int:contest_id>/classement/", show_classement_view, name="show_classement"),
    path('contest/<int:contest_id>/participant/<int:user_id>/', participant_detail_view, name='participant_detail'),
    path("contest/<int:contest_id>/teams/", manage_teams_view, name="manage_teams"),
    path("contest/settings/", salle_settings_view, name="settings"),
    path("frequentation/", salle_frequentation_view, name="frequentation"),
    path("openings/", openings_stats_view, name="openings_stats"),
    path("openings/today/", openings_stats_view, {"period": "today"}, name="openings_stats_today"),
    path("openings/<int:ouverture_id>/climbers/", opening_climbers_view, name="opening_climbers"),
    path("openings/<int:ouverture_id>/climbers/today/", opening_climbers_view, {"period": "today"}, name="opening_climbers_today"),
    path("climbers/", active_climbers_view, name="active_climbers"),
    path("climbers/<int:user_id>/progression/", climber_progression_view, name="climber_progression"),
    path("training_list/", training_list_view, name="training_list"),
    path("training/<int:user_id>/", training_calendar_view, name="training_calendar"),
]
