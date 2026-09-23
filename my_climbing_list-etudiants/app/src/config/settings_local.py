"""Bac à sable jetable : ne jamais importer les settings historiques ni dotenv."""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def required(name, expected=None):
    value = os.environ.get(name)
    if not value or (expected is not None and value != expected):
        raise ImproperlyConfigured(f"Configuration locale invalide : {name}")
    return value


DJANGO_ENV = required("DJANGO_ENV", "local")
# Compose valide le nom du projet ; sa valeur varie entre installations locales.
required("MCL_COMPOSE_PROJECT")
required("DEBUG", "True")
required("LOCAL_DB_HOST", "db")
required("LOCAL_DB_NAME", "mcl_demo")
required("LOCAL_DB_USER", "mcl_demo")
SECRET_KEY = required("LOCAL_SECRET_KEY")
if not SECRET_KEY.startswith("mcl-local-only-"):
    raise ImproperlyConfigured("LOCAL_SECRET_KEY doit être exclusivement locale")
LOCAL_DB_PASSWORD = required("LOCAL_DB_PASSWORD")
if not LOCAL_DB_PASSWORD.startswith("mcl-local-only-"):
    raise ImproperlyConfigured("LOCAL_DB_PASSWORD doit être exclusivement local")

DEBUG = True
PROD = False
PWA_ENABLED = True
APP_VERSION = "mcl-student-https-v2"
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = "local_demo.urls"
WSGI_APPLICATION = "config.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/auth/login/"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "web"]
DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql",
    "HOST": "db", "PORT": "5432", "NAME": "mcl_demo", "USER": "mcl_demo",
    "PASSWORD": LOCAL_DB_PASSWORD,
    "OPTIONS": {"connect_timeout": 5},
}}
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "MCL Démo <noreply@example.test>"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://localhost:8443", "https://127.0.0.1:8443", "https://[::1]:8443",
]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
LANGUAGE_CODE = "fr"
LANGUAGES = [("fr", "Français"), ("en", "English"), ("es", "Español"), ("pt", "Português")]
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "django_extensions", "widget_tweaks",
    "applications.custom_auth", "applications.core", "applications.services",
    "applications.reset_password", "applications.catch_all", "applications.contest",
    "applications.staff_admin", "applications.dir_admin", "applications.public_contests",
    "applications.event", "applications.route_event", "local_demo",
]
# Les migrations Django natives restent actives. Aucun second schéma à maintenir.
MIGRATION_MODULES = {name: None for name in (
    "custom_auth", "core", "contest", "staff_admin", "event", "route_event", "local_demo",
)}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "applications.staff_admin.middleware.StaffAccessMiddleware",
    "applications.dir_admin.middleware.DirAccessMiddleware",
]
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug", "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages",
        "config.context_processors.debug_context", "config.context_processors.prod_context",
        "local_demo.context.local_context",
    ]},
}]
