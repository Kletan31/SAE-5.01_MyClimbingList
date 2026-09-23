import secrets

from django.db import models


class RouteEventParticipant(models.Model):
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"

    GENDER_CHOICES = [
        (GENDER_MALE, "Homme"),
        (GENDER_FEMALE, "Femme"),
    ]

    event = models.ForeignKey(
        "route_event.RouteEvent",
        on_delete=models.CASCADE,
        related_name="participants",
    )

    phase = models.ForeignKey(
        "route_event.RouteEventPhase",
        on_delete=models.PROTECT,
        related_name="participants",
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField()

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )

    is_payment_validated = models.BooleanField(
        default=False,
    )

    access_token = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "last_name",
            "first_name",
        ]

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = secrets.token_hex(32)

        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().upper()
        self.email = self.email.strip().lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"