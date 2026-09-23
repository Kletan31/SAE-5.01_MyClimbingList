# applications/contest/models/contest_result.py

from django.db import models
from django.conf import settings
from applications.contest.models import Contest
from applications.core.models import Ouverture


class ContestResult(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name="results")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ouverture = models.ForeignKey(Ouverture, on_delete=models.CASCADE)

    has_top = models.BooleanField(default=False)
    has_zone = models.BooleanField(default=False)
    degaines_reached = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("contest", "user", "ouverture")
        verbose_name = "Résultat Contest"
        verbose_name_plural = "Résultats Contests"

    def __str__(self):
        return f"{self.user.username} - {self.ouverture} ({self.contest.name})"
