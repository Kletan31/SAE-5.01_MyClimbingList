"""Corrections PWA réservées au parcours local ; URLs historiques conservées."""
from django.urls import path

from config.urls import urlpatterns as historical_patterns
from . import views

urlpatterns = [
    path("manifest.json", views.manifest),
    path("service-worker.js", views.service_worker),
    path("register-service-worker.js", views.register_service_worker),
] + historical_patterns
