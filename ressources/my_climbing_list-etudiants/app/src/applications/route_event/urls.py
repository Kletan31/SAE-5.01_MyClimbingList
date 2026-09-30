from django.urls import path

from .views import (
    staff_login,
    staff_logout,
    staff_home,
    staff_event_list,
    staff_event_create,
    staff_event_update,
    staff_event_delete,
    staff_phase_create,
    staff_phase_update,
    staff_phase_delete,
    staff_route_list,
    staff_delete_route,
    route_event_home,
    route_event_register,
    participant_access,
    staff_participant_list,
    staff_validate_participant,
    staff_unvalidate_participant,
    staff_delete_participant,
    staff_resend_participant_link,
    participant_ranking,
    staff_ranking,
    staff_ranking_display,
    participant_route_rankings,
    public_ranking,
    public_route_rankings,
    staff_route_rankings,
    staff_move_route_up,
    staff_move_route_down,
    staff_ranking_export_csv,
    staff_ranking_export_pdf,
    staff_participant_update,
)

app_name = "route_event"

urlpatterns = [
    path("staff/login/", staff_login, name="staff_login"),
    path("staff/logout/", staff_logout, name="staff_logout"),
    path("staff/", staff_home, name="staff_home"),

    path("staff/events/", staff_event_list, name="staff_event_list"),
    path("staff/events/create/", staff_event_create, name="staff_event_create"),
    path("staff/events/<slug:slug>/edit/", staff_event_update, name="staff_event_update"),
    path("staff/events/<slug:slug>/delete/", staff_event_delete, name="staff_event_delete"),

    path("staff/events/<slug:slug>/phases/create/", staff_phase_create, name="staff_phase_create"),
    path("staff/phases/<int:phase_id>/edit/", staff_phase_update, name="staff_phase_update"),
    path("staff/phases/<int:phase_id>/delete/", staff_phase_delete, name="staff_phase_delete"),

    path("staff/<slug:slug>/routes/", staff_route_list, name="staff_route_list"),
    path("staff/route/<int:route_id>/delete/", staff_delete_route, name="staff_delete_route"),

    path("", route_event_home, name="home"),
    path("<slug:slug>/register/", route_event_register, name="register"),
    path("participant/<str:token>/", participant_access, name="participant_access"),

    path("staff/<slug:slug>/participants/", staff_participant_list, name="staff_participant_list"),
    path("staff/participant/<int:participant_id>/validate/", staff_validate_participant, name="staff_validate_participant"),
    path("staff/participant/<int:participant_id>/unvalidate/", staff_unvalidate_participant, name="staff_unvalidate_participant"),
    path("staff/participant/<int:participant_id>/delete/", staff_delete_participant, name="staff_delete_participant"),
    path("staff/participant/<int:participant_id>/resend-link/", staff_resend_participant_link, name="staff_resend_participant_link"),

    path("participant/<str:token>/ranking/", participant_ranking, name="participant_ranking"),
    path("staff/<slug:slug>/ranking/", staff_ranking, name="staff_ranking"),

    path("staff/<slug:slug>/display/", staff_ranking_display, name="staff_ranking_display"),

    path("participant/<str:token>/route-rankings/", participant_route_rankings, name="participant_route_rankings"),
    path("<slug:slug>/ranking/", public_ranking, name="public_ranking"),
    path("<slug:slug>/route-rankings/", public_route_rankings, name="public_route_rankings"),
    path("staff/<slug:slug>/route-rankings/", staff_route_rankings, name="staff_route_rankings"),

    path("staff/routes/<int:route_id>/up/", staff_move_route_up, name="staff_move_route_up"),
    path("staff/routes/<int:route_id>/down/", staff_move_route_down, name="staff_move_route_down"),

    path("staff/<slug:slug>/ranking/export/csv/", staff_ranking_export_csv, name="staff_ranking_export_csv"),
    path("staff/<slug:slug>/ranking/export/pdf/", staff_ranking_export_pdf, name="staff_ranking_export_pdf"),

    path("staff/participant/<int:participant_id>/edit/", staff_participant_update, name="staff_participant_update"),
]