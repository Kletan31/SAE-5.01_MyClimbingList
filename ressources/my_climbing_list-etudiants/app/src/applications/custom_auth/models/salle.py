# applications/custom_auth/models/salle.py

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Salle(models.Model):
    """Modèle représentant une salle d'escalade avec des relais pour grimpe en tête."""

    id = models.IntegerField(primary_key=True)  # Identifiant unique pour chaque salle
    nom = models.CharField(max_length=100)  # Nom de la salle
    relais_en_tete = ArrayField(models.IntegerField(), blank=True, default=list)  # Liste des relais disponibles
    masquer_cotation_recentes = models.BooleanField(default=False)  # Option pour cacher les cotations

    def __str__(self):
        return self.nom
