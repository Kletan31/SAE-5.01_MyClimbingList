# applications/service/urls_non_i18n.py
from django.urls import path, re_path
from . import views
from django.conf import settings

app_name = 'services'

urlpatterns = [

    # === PWA === #
    path('manifest.json', views.manifest_view, name='manifest'),
    path('register-service-worker.js', views.register_service_worker_view, name='register-service-worker'),
    path('sw-placeholder.js', views.sw_placeholder_view, name='sw-placeholder'),
    path('service-worker.js', views.service_worker_view, name='service-worker'),

    # === Viewport Height === #
    path('set-viewport-dimensions/', views.set_viewport_dimensions_view, name='set_viewport_height'),

    # === Suppression du compte === #
    path('delete-account/', views.delete_account_view, name='delete_account'),

    # === Gestion de la popup d'information === #
    path('mark_popup_seen/', views.mark_popup_seen_view, name='mark_popup_seen'),
]

# === Gestion des fichiers statiques en mode DEBUG === #
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', views.custom_static_serve, name='serve_static'),
    ]
