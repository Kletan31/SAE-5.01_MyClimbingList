from django.db import models


class EventPhase(models.Model):
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="phases")

    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    capacity = models.PositiveIntegerField(default=50)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.event.name} - {self.name}"