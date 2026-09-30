# applications/contest/models/contest.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from applications.core.models import Ouverture
from applications.custom_auth.models import Salle


class Contest(models.Model):
    # =========================
    # FORMATS
    # =========================
    CLASSIC = "classic"
    POINTS_1000 = "1000_points"
    FORMAT_CHOICES = [
        (CLASSIC, "Classique"),
        (POINTS_1000, "1000 points"),
    ]

    # =========================
    # DISCIPLINES
    # =========================
    BLOC = "bloc"
    VOIE = "voie"
    DISCIPLINE_CHOICES = [
        (BLOC, "Bloc"),
        (VOIE, "Voie"),
    ]

    # =========================
    # CHAMPS
    # =========================
    name = models.CharField(max_length=255)

    description_courte = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Description courte",
    )
    description = models.TextField(blank=True)

    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)

    ouvertures = models.ManyToManyField(
        Ouverture,
        related_name="contests",
    )

    # REMPLI AUTOMATIQUEMENT
    discipline = models.CharField(
        max_length=10,
        choices=DISCIPLINE_CHOICES,
        null=True,
        blank=True,
        help_text="Déduit automatiquement à partir des ouvertures",
    )

    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        default=CLASSIC,
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # =========================
    # CONTEST DE DÉPART
    # =========================
    initial_contest = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="derived_contests",
        help_text="Contest terminé et non permanent servant de base de score",
        verbose_name="Lier un contest",
    )

    # =========================
    # OPTIONS
    # =========================
    is_active = models.BooleanField(default=True, verbose_name="Visible")
    is_payant = models.BooleanField(default=False, verbose_name="Payant")
    is_team_contest = models.BooleanField(
        default=False,
        verbose_name="Contest par équipe",
    )

    is_permanent = models.BooleanField(default=False)
    is_permanent_enabled = models.BooleanField(default=False)

    has_zone = models.BooleanField(default=False, verbose_name="Zones")
    has_degaine = models.BooleanField(default=False, verbose_name="Dégaines")
    hide_cotation = models.BooleanField(default=False, verbose_name="Masquer les cotations")
    sort_by_name = models.BooleanField(default=False, verbose_name="Trier par nom")

    # REMPLI AUTOMATIQUEMENT
    is_combine = models.BooleanField(default=False)

    # =========================
    # QUOTA
    # =========================
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Laisser vide pour illimité.",
    )

    # =========================
    # MÉTADONNÉES
    # =========================
    def __str__(self) -> str:
        return self.name

    # =========================
    # PROPRIÉTÉS
    # =========================
    @property
    def is_running(self) -> bool:
        now_ = now()
        if not self.is_active:
            return False
        if self.end_date is None:
            return self.start_date <= now_
        return self.start_date <= now_ <= self.end_date

    @property
    def accepted_count(self) -> int:
        return self.inscriptions.filter(status="accepted").count()

    @property
    def pending_count(self) -> int:
        return self.inscriptions.filter(status="pending").count()

    @property
    def is_unlimited(self) -> bool:
        return self.max_participants is None

    @property
    def is_full(self) -> bool:
        return (not self.is_unlimited) and (
            self.accepted_count >= self.max_participants
        )

    @property
    def remaining_slots(self):
        if self.is_unlimited:
            return None
        return max(self.max_participants - self.accepted_count, 0)

    def can_accept(self, n: int = 1) -> bool:
        if self.is_unlimited:
            return True
        return (self.accepted_count + n) <= self.max_participants

    # =========================
    # LOGIQUE MÉTIER (M2M SAFE)
    # =========================
    def update_discipline_from_ouvertures(self):
        """
        Détermine automatiquement :
        - discipline (Bloc / Voie / None)
        - is_combine

        DOIT être appelé après save_m2m().
        """
        ouvertures = self.ouvertures.all()

        if not ouvertures.exists():
            self.discipline = None
            self.is_combine = False
            return

        blocs = {o.bloc for o in ouvertures}

        if len(blocs) > 1:
            self.discipline = None
            self.is_combine = True
        else:
            self.discipline = Contest.BLOC if True in blocs else Contest.VOIE
            self.is_combine = False

    # =========================
    # VALIDATION MÉTIER (SANS M2M)
    # =========================
    def clean(self):
        # --- Dates
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError({
                "end_date": "La date de fin doit être postérieure à la date de début."
            })

        # --- Quota
        if self.max_participants == 0:
            raise ValidationError({
                "max_participants": "Laisser vide pour illimité."
            })

        # --- INTERDICTION : équipe + zone / dégaine
        if self.is_team_contest and (self.has_zone or self.has_degaine):
            raise ValidationError(
                "Un contest par équipe ne peut pas utiliser les zones ou les dégaines."
            )

        # --- VALIDATION CONTEST DE DÉPART
        if self.initial_contest:
            if self.initial_contest.is_permanent:
                raise ValidationError({
                    "initial_contest": "Le contest de départ ne peut pas être permanent."
                })

            if not self.initial_contest.end_date or self.initial_contest.end_date >= now():
                raise ValidationError({
                    "initial_contest": "Le contest de départ doit être terminé."
                })

            if self.initial_contest == self:
                raise ValidationError({
                    "initial_contest": (
                        "Un contest ne peut pas être son propre contest de départ."
                    )
                })

            # --- INTERDICTION : équipe + contest de départ
            if self.is_team_contest:
                raise ValidationError({
                    "initial_contest": (
                        "Un contest par équipe ne peut pas être lié à un contest de départ."
                    )
                })
