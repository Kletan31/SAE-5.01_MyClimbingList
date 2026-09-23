from django.urls import path
from . import views
from . import refresh_views

app_name = 'core'

urlpatterns = [
    # Home
    path('home/', views.home_view, name='home'),
    path('load_more_sessions/', refresh_views.load_more_sessions, name='load_more_sessions'),

    # Liste des salles
    path('list/', views.salle_list_view, name='list'),
    path("favorite/toggle/", refresh_views.toggle_favorite_salle, name="toggle_favorite_salle"),

    # Propriétés de la salle
    path('properties/<int:salle_id>/', views.gym_properties_view, name='properties'),
    path('properties/refresh/', refresh_views.gym_properties_refresh, name='properties_refresh'),

    # Guidebook
    path('guidebook/', views.guidebook_view, name='guidebook'),

    # Session
    path('confirm_session/', views.confirm_session_view, name='confirm_session'),

    # Graph
    path('graph/', views.graph_view, name='graph'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Paramètres
    path('settings/', views.settings_view, name='settings'),

    # Feedback
    path('feedback/', views.feedback_view, name='feedback'),

    # Carnet
    path('logbook/', views.logbook_view, name='logbook'),

    # Projets
    path('projects/', views.projects_view, name='projects'),
    path('projects/refresh/', refresh_views.project_refresh, name='projects_refresh'),

    # Détails
    path('details/', views.details_view, name='details'),

    # Offline
    path('offline/', views.offline_view, name='offline'),

    # Training
    path('training/', views.training_view, name='training'),
]
