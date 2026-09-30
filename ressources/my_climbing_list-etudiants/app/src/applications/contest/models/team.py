# applications/contest/models/team.py

from django.db import models
from django.contrib.auth import get_user_model
from applications.contest.models import Contest

User = get_user_model()


class Team(models.Model):
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name="teams",
        verbose_name="Contest associé"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de l'équipe"
    )
    members = models.ManyToManyField(
        User,
        related_name="teams",
        verbose_name="Membres de l'équipe",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("contest", "name")
        verbose_name = "Équipe"
        verbose_name_plural = "Équipes"

    def __str__(self):
        return f"{self.name} ({self.contest.name})"
