# applications/core/models/seance.py

from django.db import models
from django.contrib.auth.models import User
from datetime import date
from applications.core.models import Ouverture


class Seance(models.Model):
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ouverture = models.ForeignKey(Ouverture, on_delete=models.CASCADE)

    # Données sportives
    date_seance = models.DateField(default=date.today)
    nb_top = models.IntegerField(default=0)
    nb_try = models.IntegerField(default=0)
    nb_top_lead = models.IntegerField(default=0)
    nb_try_lead = models.IntegerField(default=0)

    flash = models.BooleanField(default=False)
    flash_lead = models.BooleanField(default=False)
    flash_available = models.BooleanField(default=True)
    is_project_visible = models.BooleanField(default=True)

    # Métadonnées temporelles (clé pour l’Elo journalier)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_seance"]

    def __str__(self):
        return (
            f"Seance {self.user.username} - "
            f"{self.ouverture.niveau} - "
            f"{self.nb_try} - "
            f"{self.date_seance}"
        )
