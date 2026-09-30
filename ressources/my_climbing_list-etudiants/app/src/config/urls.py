# Imports
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf.urls.i18n import i18n_patterns

# === URLs NON traduites === #
non_i18n_urlpatterns = [
    # === Services === #
    path('', include('applications.services.urls_non_i18n')),                   # APP Utilitaire

    # === set_language === #
    path("i18n/", include("django.conf.urls.i18n")),                            # Active la vue set_language
]

# === URLs traduites === #
i18n_urlpatterns = i18n_patterns(
    # === Root URL === #
    path('', RedirectView.as_view(pattern_name="core:home")),             # URL Racine

    # === Authentification === #
    path('auth/', include('applications.custom_auth.urls')),                    # APP Authentification

    # === Services (seulement les vues traduites) === #
    path('', include('applications.services.urls_i18n')),                       # APP Services

    # === Reset_password === #
    path('', include('applications.reset_password.urls')),                      # APP Mot De Passe Oublié

    # === Applications === #
    path('core/', include('applications.core.urls')),                           # APP Principale

    # === Contest === #
    path('contest/', include('applications.contest.urls')),                     # APP Contest

    # === Event === #
    path('event/', include('applications.event.urls')),                         # APP Event

    # === Route Event === #
    path('route_event/', include('applications.route_event.urls')),             # APP Route Event

    # === Public_contest === #
    path('public_contests/', include('applications.public_contests.urls')),     # APP Public Contests

    # === Staff === #
    path('staff/', include('applications.staff_admin.urls')),                   # APP Staff

    # === Direction === #
    path('direction/', include('applications.dir_admin.urls')),                 # APP Direction

    # === Catch_All === #
    path('<path:resource>', include('applications.catch_all.urls')),            # APP Catch-All
)

urlpatterns = non_i18n_urlpatterns + i18n_urlpatterns
