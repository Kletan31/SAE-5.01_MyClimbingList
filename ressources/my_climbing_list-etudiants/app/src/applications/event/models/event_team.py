import secrets

from django.core.exceptions import ValidationError
from django.db import models


class EventTeam(models.Model):
    TEAM_TYPE_MALE = "M"
    TEAM_TYPE_FEMALE = "F"
    TEAM_TYPE_MIXED = "X"

    TEAM_TYPE_CHOICES = [
        (TEAM_TYPE_MALE, "Duo homme"),
        (TEAM_TYPE_FEMALE, "Duo femme"),
        (TEAM_TYPE_MIXED, "Duo mixte"),
    ]

    event = models.ForeignKey(
        "event.Event",
        on_delete=models.CASCADE,
        related_name="teams"
    )

    participant_1 = models.ForeignKey(
        "event.EventParticipant",
        on_delete=models.CASCADE,
        related_name="teams_as_first_member"
    )

    participant_2 = models.ForeignKey(
        "event.EventParticipant",
        on_delete=models.CASCADE,
        related_name="teams_as_second_member"
    )

    phase = models.ForeignKey(
        "event.EventPhase",
        on_delete=models.PROTECT,
        related_name="teams"
    )

    team_type = models.CharField(
        max_length=1,
        choices=TEAM_TYPE_CHOICES,
        editable=False
    )

    is_payment_validated = models.BooleanField(default=False)

    access_token = models.CharField(
        max_length=64,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def compute_team_type(self):
        if self.participant_1.gender != self.participant_2.gender:
            return self.TEAM_TYPE_MIXED

        if self.participant_1.gender == "M":
            return self.TEAM_TYPE_MALE

        return self.TEAM_TYPE_FEMALE

    def clean(self):
        if self.participant_1_id == self.participant_2_id:
            raise ValidationError(
                "Un duo ne peut pas contenir deux fois le même participant."
            )

        if (
            self.participant_1.event_id != self.event_id
            or self.participant_2.event_id != self.event_id
        ):
            raise ValidationError(
                "Les participants doivent appartenir au même événement que l’équipe."
            )

        if self.phase.event_id != self.event_id:
            raise ValidationError(
                "La phase sélectionnée n’appartient pas à cet événement."
            )

        existing_team_for_p1 = EventTeam.objects.filter(
            event=self.event,
        ).filter(
            models.Q(participant_1=self.participant_1)
            | models.Q(participant_2=self.participant_1)
        )

        if self.pk:
            existing_team_for_p1 = existing_team_for_p1.exclude(pk=self.pk)

        if existing_team_for_p1.exists():
            raise ValidationError(
                f"{self.participant_1} appartient déjà à un duo pour cet événement."
            )

        existing_team_for_p2 = EventTeam.objects.filter(
            event=self.event,
        ).filter(
            models.Q(participant_1=self.participant_2)
            | models.Q(participant_2=self.participant_2)
        )

        if self.pk:
            existing_team_for_p2 = existing_team_for_p2.exclude(pk=self.pk)

        if existing_team_for_p2.exists():
            raise ValidationError(
                f"{self.participant_2} appartient déjà à un duo pour cet événement."
            )

        team_count_in_phase = EventTeam.objects.filter(
            phase=self.phase,
        )

        if self.pk:
            team_count_in_phase = team_count_in_phase.exclude(pk=self.pk)

        if team_count_in_phase.count() >= self.phase.capacity:
            raise ValidationError("Ce créneau est complet.")

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = secrets.token_hex(32)

        self.team_type = self.compute_team_type()

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.participant_1} / {self.participant_2}"