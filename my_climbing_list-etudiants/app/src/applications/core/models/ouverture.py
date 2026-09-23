# applications/core/models/ouverture.py

# Modules
from django.db import models
from applications.custom_auth.models import Salle


# Table des ouvertures
class Ouverture(models.Model):
    id = models.IntegerField(primary_key=True)                                  # Identifiant unique de l'ouverture
    active = models.BooleanField(default=True)                                  # Définie si l'ouverture boulonnée ou non
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)                  # Relation vers le modèle Salle
    bloc = models.BooleanField(default=False)                                   # Définie si l'ouverture est un bloc ou non
    relais = models.IntegerField()                                              # Numéro de relais/secteur de l'ouverture
    niveau = models.CharField(max_length=50)                                    # Cotation
    niveau_couleur = models.CharField(max_length=11, blank=True, default="")    # Couleur HEX associée à la cotation
    couleur = models.CharField(max_length=50)                                   # Couleur des prises
    hex_couleur = models.CharField(max_length=11, blank=True, default="")       # Couleur HEX
    date_ouverture = models.DateField()                                         # Date d'ouverture
    nom = models.CharField(max_length=100)                                      # Nom de l'ouverture
    ouvreur = models.CharField(max_length=100, blank=True, default="")          # Ouvreur
    profil = models.CharField(max_length=100, blank=True, default="")           # Profil (Dièdre, vertical, dévers, etc.)
    style = models.CharField(max_length=100, blank=True, default="")            # Style (Rési, Conti, Bloc)

    def __str__(self):
        return f"Secteur {self.relais}: {self.niveau} [{self.couleur}]" if self.bloc else f"Relais {self.relais}: {self.niveau} [{self.couleur}]"
