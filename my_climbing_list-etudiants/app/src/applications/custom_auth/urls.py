from django.urls import path
from . import views

app_name = 'custom_auth'

urlpatterns = [
    # Connexion
    path('login/', views.login_view, name='login'),

    # Inscription
    path('register/', views.register_view, name='register'),

    # Déconnexion
    path('logout/', views.logout_view, name='logout'),

    # Support
    path('support/', views.support_view, name='login_support'),

    # Offline
    path('offline/', views.offline_view, name='offline'),
]
