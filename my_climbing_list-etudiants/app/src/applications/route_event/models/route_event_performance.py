from django.core.exceptions import ValidationError
from django.db import models


class RouteEventPerformance(models.Model):
    participant = models.ForeignKey(
        "route_event.RouteEventParticipant",
        on_delete=models.CASCADE,
        related_name="performances",
    )

    route = models.ForeignKey(
        "route_event.RouteEventRoute",
        on_delete=models.CASCADE,
        related_name="performances",
    )

    hold_number = models.PositiveIntegerField(default=0)
    hold_plus = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant", "route"],
                name="unique_route_event_performance_per_participant_and_route",
            )
        ]

    def clean(self):
        if self.participant.event_id != self.route.event_id:
            raise ValidationError(
                "Le participant et la voie doivent appartenir au même événement."
            )

        if self.hold_number == 0 and self.hold_plus:
            raise ValidationError(
                "Le symbole + ne peut pas être utilisé sans prise atteinte."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        suffix = "+" if self.hold_plus else ""
        return f"{self.participant} - {self.route} : {self.hold_number}{suffix}"