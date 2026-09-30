# applications/custom_auth/models/profile.py

from django.db import models
from django.contrib.auth.models import User
from applications.custom_auth.models import Salle


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Neutral'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # --- Salles par discipline ---
    salle_voie = models.ForeignKey(
        Salle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles_voie",
        help_text="Salle associée à la pratique de la voie"
    )

    salle_bloc = models.ForeignKey(
        Salle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles_bloc",
        help_text="Salle associée à la pratique du bloc"
    )

    # --- Salle favorite ---
    favorite_salle = models.ForeignKey(
        Salle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favorited_by_users",
        help_text="Salle favorite de l'utilisateur"
    )

    # --- Accès aux séances ---
    authorized_salles = models.ManyToManyField(
        Salle,
        blank=True,
        related_name="authorized_profiles",
        help_text="Salles autorisées à accéder aux séances de l'utilisateur"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        default="",
    )

    def __str__(self):
        parts = []
        if self.salle_voie:
            parts.append(f"Voie: {self.salle_voie.nom}")
        if self.salle_bloc:
            parts.append(f"Bloc: {self.salle_bloc.nom}")

        salles = " | ".join(parts) if parts else "No Salle"
        return f"{self.user.username} - {salles}"
