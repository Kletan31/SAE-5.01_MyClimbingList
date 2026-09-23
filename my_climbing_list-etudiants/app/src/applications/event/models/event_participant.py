from django.db import models


class EventParticipant(models.Model):
    GENDER_MALE = "M"
    GENDER_FEMALE = "F"

    GENDER_CHOICES = [
        (GENDER_MALE, "Homme"),
        (GENDER_FEMALE, "Femme"),
    ]

    event = models.ForeignKey(
        "event.Event",
        on_delete=models.CASCADE,
        related_name="participants",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().upper()
        self.email = self.email.strip().lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"