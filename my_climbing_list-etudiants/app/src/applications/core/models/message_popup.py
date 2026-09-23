from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language


class MessagePopup(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="Identifiant unique du message (ex: 'v2.1')")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def get_translation(self, lang_code=None):
        lang = lang_code or get_language() or 'fr'
        translation = self.translations.filter(language=lang).first()
        if not translation:
            translation = self.translations.filter(language='en').first() or self.translations.first()
        return translation


class MessagePopupTranslation(models.Model):
    popup = models.ForeignKey(MessagePopup, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=5, choices=[
        ('fr', 'Français'),
        ('en', 'English'),
        ('es', 'Español'),
        ('pt', 'Português'),
    ])
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        unique_together = ('popup', 'language')

    def __str__(self):
        return f"{self.popup.code} ({self.language})"


class MessagePopupView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    popup = models.ForeignKey(MessagePopup, on_delete=models.CASCADE)
    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'popup')

    def __str__(self):
        return f"{self.user.username} a vu {self.popup.code} à {self.seen_at}"
