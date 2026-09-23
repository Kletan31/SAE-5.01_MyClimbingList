from django.core.exceptions import ValidationError
from django.db import models

from applications.core.models import Ouverture


class EventRoute(models.Model):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="routes")
    ouverture = models.ForeignKey(Ouverture, on_delete=models.CASCADE, related_name="event_routes")

    points = models.PositiveIntegerField(default=1)
    has_zone = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "ouverture__relais", "ouverture__id"]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "ouverture"],
                name="unique_event_route_per_event"
            )
        ]

    def clean(self):
        if not self.event_id and not getattr(self, "event", None):
            return

        if not self.ouverture_id and not getattr(self, "ouverture", None):
            return

        if self.ouverture.salle_id != self.event.salle_id:
            raise ValidationError("Cette ouverture n’appartient pas à la salle de l’événement.")

        if not self.ouverture.bloc:
            raise ValidationError("Seuls des blocs peuvent être associés à cet événement.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name} - {self.ouverture}"