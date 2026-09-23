# applications/contest/apps.py

from django.apps import AppConfig


class ContestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.contest"

    def ready(self):
        # Enregistre les receivers de signaux
        from . import signals  # noqa: F401
