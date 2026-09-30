from django.core.exceptions import ValidationError
from django.db import models

from applications.core.models import Ouverture


class RouteEventRoute(models.Model):
    event = models.ForeignKey(
        "route_event.RouteEvent",
        on_delete=models.CASCADE,
        related_name="routes",
    )

    ouverture = models.ForeignKey(
        Ouverture,
        on_delete=models.CASCADE,
        related_name="route_event_routes",
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            "display_order",
            "ouverture__relais",
            "ouverture__id",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["event", "ouverture"],
                name="unique_route_event_route_per_event",
            ),
            models.UniqueConstraint(
                fields=["event", "display_order"],
                name="unique_route_event_route_order_per_event",
            ),
        ]

    def clean(self):
        if not self.event_id and not getattr(self, "event", None):
            return

        if not self.ouverture_id and not getattr(self, "ouverture", None):
            return

        if self.ouverture.salle_id != self.event.salle_id:
            raise ValidationError(
                "Cette voie n’appartient pas à la salle de l’événement."
            )

        if self.ouverture.bloc:
            raise ValidationError(
                "Seules des voies peuvent être associées à cet événement."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name} - {self.ouverture}"