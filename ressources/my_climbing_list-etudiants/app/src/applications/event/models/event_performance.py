from django.core.exceptions import ValidationError
from django.db import models


class EventPerformance(models.Model):
    participant = models.ForeignKey(
        "event.EventParticipant",
        on_delete=models.CASCADE,
        related_name="performances"
    )
    route = models.ForeignKey(
        "event.EventRoute",
        on_delete=models.CASCADE,
        related_name="performances"
    )

    top = models.BooleanField(default=False)
    zone = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant", "route"],
                name="unique_event_performance_per_participant_and_route"
            )
        ]

    def clean(self):
        if self.participant.event_id != self.route.event_id:
            raise ValidationError("Le participant et le bloc doivent appartenir au même événement.")

        if self.top and not self.zone and self.route.has_zone:
            raise ValidationError("Un top sur un bloc avec zone implique nécessairement la zone.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant} - {self.route}"