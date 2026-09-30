# applications/staff_admin/models/climber_level_daily.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ClimberLevelDaily(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bloc = models.BooleanField()
    date = models.DateField()

    # -----------------------------
    # Données Elo journalières
    # -----------------------------
    elo = models.FloatField(null=True, blank=True)

    elo_trend = models.CharField(
        max_length=4,
        choices=(
            ("up", "Up"),
            ("down", "Down"),
        ),
        null=True,
        blank=True,
        help_text="Tendance Elo sur les 7 derniers jours (up / down / null)",
    )

    level = models.CharField(max_length=4, default="-")
    color = models.CharField(max_length=16, default="#333")

    class Meta:
        unique_together = ("user", "bloc", "date")
        indexes = [
            models.Index(fields=["user", "bloc", "date"]),
        ]

    def __str__(self):
        return (
            f"{self.user.username} | "
            f"{'Bloc' if self.bloc else 'Voie'} | "
            f"{self.date} | "
            f"Elo={int(self.elo) if self.elo else '-'} "
            f"({self.elo_trend or '–'})"
        )
