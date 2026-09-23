# applications/reset_password/views.py
from pathlib import Path
from django.contrib.auth.views import PasswordResetView
from django.utils import translation


def localized_template(template_name: str, lang: str) -> str:
    """
    Retourne le chemin du template localisé correspondant à la langue active.
    Exemple :
        'reset_password/email_templates/html/password_reset_email.html'
    devient :
        'reset_password/email_templates/html/en/password_reset_email.html'
    """
    p = Path(template_name)
    localized_path = p.parent / lang / p.name
    return str(localized_path)


class CustomPasswordResetView(PasswordResetView):
    """
    Utilise automatiquement la version localisée des templates d'e-mail
    selon la langue active de l'utilisateur ou de l'URL.
    """
    def form_valid(self, form):
        # Détection de la langue active
        lang = translation.get_language_from_request(self.request, check_path=True) or "fr"

        # Remplacement direct des chemins par leur version localisée
        self.email_template_name = localized_template(self.email_template_name, lang)
        self.html_email_template_name = localized_template(self.html_email_template_name, lang)
        self.subject_template_name = localized_template(self.subject_template_name, lang)

        # Force le rendu dans la langue correspondante
        with translation.override(lang):
            return super().form_valid(form)
