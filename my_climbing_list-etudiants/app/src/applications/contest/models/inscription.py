# applications/contest/models/inscription.py

from django.db import models
from django.conf import settings
from applications.contest.models import Contest


class Inscription(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        ACCEPTED = "accepted", "Acceptée"
        REFUSED = "refused", "Refusée"

        choices: tuple  # <-- aide PyCharm, ne change rien à l’exécution

    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        related_name="inscriptions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="inscriptions"
    )
    date_inscription = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    # =========================
    # NOUVEAU — SCORE INITIAL
    # =========================
    score_initial = models.IntegerField(
        null=True,
        blank=True,
        help_text="Score de départ hérité d’un contest précédent"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["contest", "user"],
                name="uniq_contest_user"
            ),
        ]

    def is_active(self):
        """
        Retourne True si l'inscription est active, selon le type de contest.
        - Payant : actif si ACCEPTED.
        - Gratuit : actif même en PENDING (comme avant), mais REFUSED n'est jamais actif.
        """
        if self.status == self.Status.REFUSED:
            return False
        if self.contest.is_payant:
            return self.status == self.Status.ACCEPTED
        return True  # gratuit

    def __str__(self):
        return f"{self.user} – {self.contest} ({self.get_status_display()})"
