# applications/service/urls_i18n.py
from django.urls import path
from . import views

app_name = 'services_i18n'

urlpatterns = [
    # === Maintenance === #
    path('offline/', views.offline_view, name='offline'),

    # === Guide d'installation === #
    path('install-guide/', views.install_guide_view, name='install_guide'),
]
