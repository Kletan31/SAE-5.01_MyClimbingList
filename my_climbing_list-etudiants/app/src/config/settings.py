"""Référence historique assainie, volontairement non exécutable."""
raise RuntimeError("Utiliser exclusivement config.settings_local avec Docker local")

# === Importations ===
import os
from pathlib import Path
from dotenv import load_dotenv
import platform
import time
from django.utils.translation import gettext_lazy as _

# === Chargement des variables d'environnement ===
load_dotenv()

# === Variables ===
SECRET_KEY = os.environ["HISTORICAL_SECRET_KEY"]
PROD = platform.system() != 'Darwin'                    # Mode PRODUCTION
DEBUG = os.getenv('DEBUG', 'False') == 'True'           # Mode DEBUG
APP_VERSION = str(int(time.time()))                     # Version de l'application
BASE_DIR = Path(__file__).resolve().parent.parent       # Racine du projet
ROOT_URLCONF = 'config.urls'                            # Fichier urls racine
WSGI_APPLICATION = 'config.wsgi.application'            # Application WSGI
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'    # Format des ID de la base de données
LOGIN_URL = '/auth/login/'                              # Page de connexion
PASSWORD_RESET_TIMEOUT = 3600                           # Expiration du lien de réinitialisation

# === Activer HTTP Strict Transport Security ===
SECURE_HSTS_SECONDS = 31536000              # Pendant 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True       # Inclure les sous-domaines
SECURE_HSTS_PRELOAD = True                  # Bloquer l’accès en HTTP avant même la première connexion

# === Forcer la redirection HTTPS ===
SECURE_SSL_REDIRECT = True                                      # Doublons avec Nginx (mesure de sécurité)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')   # Récupération du protocole utilisé par le client

# === Sécuriser les cookies ===
SESSION_COOKIE_SECURE = True    # Empêche les sessions Django d’être envoyées en HTTP
CSRF_COOKIE_SECURE = True       # Empêche les jetons CSRF d’être envoyées en HTTP

# === Règles de validation des mots de passe ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Paramètres d'internationalisation ===
LANGUAGE_CODE = 'fr'

LANGUAGES = [
    ("fr", _("French")),
    ("en", _("English")),
    ("es", _("Spanish")),
    ("pt", _("Portuguese")),
]

TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# === Configuration des fichiers statiques ===
STATIC_URL = 'static/'                          # URL pour servir les fichiers statiques
STATICFILES_DIRS = [BASE_DIR / "static"]        # Répertoire des fichiers statiques
STATIC_ROOT = BASE_DIR / "staticfiles"          # Répertoire pour collectstatic

# === Configuration des emails (SMTP OVH) ===
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = 465                                                # Port SMTP sécurisé SSL
EMAIL_USE_SSL = True                                            # Utilisation de SSL (port 465)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")

# === Hôtes autorisés et paramètres CSRF ===
ALLOWED_HOSTS = ['mcl.example.test'] if PROD else ['*']
CSRF_TRUSTED_ORIGINS = ['https://mcl.example.test'] if PROD else ['https://localhost']
CSRF_FAILURE_VIEW = "applications.services.views.csrf_failure_view"

# === Applications Django natives ===
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# === Applications tierces ===
THIRD_PARTY_APPS = [
    'django_extensions',    # Ajoute la commande "runserver_plus"
    'custom_migrations',    # Applique des migrations spécifiques
    'widget_tweaks',        # Stylise les champs de formulaire dans les templates
]

# === Applications internes ===
LOCAL_APPS = [
    'applications.custom_auth',
    'applications.core',
    'applications.services',
    'applications.reset_password',
    'applications.catch_all',
    'applications.contest',
    'applications.staff_admin',
    'applications.dir_admin',
    'applications.public_contests',
    'applications.event',
    'applications.route_event',
]

# === Applications installées ===
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'applications.staff_admin.middleware.StaffAccessMiddleware',    # Gestion du routing dans staff_admin
    'applications.dir_admin.middleware.DirAccessMiddleware',        # Gestion du routing dans dir_admin
]

if not PROD:
    MIDDLEWARE.insert(0, 'config.middleware.NoStoreCacheMiddleware')

# === Configuration des templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Répertoire des templates de base
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.debug_context',
                'config.context_processors.prod_context',
            ],
        },
    },
]

# === Configuration de la base de données ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# === Gestion du stockage des fichiers ===
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",  # Ajoute un hash au nom du fichier
    },
}
