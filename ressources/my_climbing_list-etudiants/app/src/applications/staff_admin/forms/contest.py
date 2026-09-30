# applications/staff_admin/forms/contest.py

from datetime import timedelta

from django import forms
from django.utils.timezone import localtime, now

from applications.contest.models import Contest
from applications.core.models import Ouverture


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        exclude = [
            "salle",
            "created_by",
            "discipline",
            "is_combine",
            "is_permanent",
            "is_permanent_enabled",
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        salle = getattr(user.profile, "favorite_salle", None)
        now_ = now()
        six_months_ago = now_ - timedelta(days=180)

        if salle:
            # ----------------------------
            # OUVERTURES (restreintes à la salle)
            # ----------------------------
            self.fields["ouvertures"].queryset = (
                Ouverture.objects
                .filter(salle=salle, active=True)
                .order_by("-bloc", "relais")
            )

        # ----------------------------
        # CONTEST DE DÉPART
        # - inter-salles autorisé
        # - non permanent
        # - terminé
        # - moins de 6 mois
        # ----------------------------
        if "initial_contest" in self.fields:
            self.fields["initial_contest"].queryset = (
                Contest.objects
                .filter(
                    is_permanent=False,
                    end_date__isnull=False,
                    end_date__lt=now_,
                    end_date__gte=six_months_ago,
                )
                .order_by("-end_date")
            )

        # ----------------------------
        # Conversion datetime → datetime-local
        # ----------------------------
        for field in ("start_date", "end_date"):
            value = getattr(self.instance, field, None)
            if value:
                self.initial[field] = localtime(value).strftime("%Y-%m-%dT%H:%M")

    # =========================
    # VALIDATION MÉTIER (M2M OK)
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        ouvertures = cleaned_data.get("ouvertures")
        is_team_contest = cleaned_data.get("is_team_contest")
        has_zone = cleaned_data.get("has_zone")
        has_degaine = cleaned_data.get("has_degaine")
        initial_contest = cleaned_data.get("initial_contest")

        # ---------------------------------
        # AU MOINS UNE OUVERTURE OBLIGATOIRE
        # ---------------------------------
        if not ouvertures:
            self.add_error(
                "ouvertures",
                "Vous devez sélectionner au moins une ouverture pour créer un contest."
            )
            return cleaned_data

        # ---------------------------------
        # Discipline / combiné (source de vérité)
        # ---------------------------------
        blocs = {o.bloc for o in ouvertures}

        if len(blocs) > 1:
            cleaned_data["discipline"] = None
            cleaned_data["is_combine"] = True
        else:
            cleaned_data["discipline"] = (
                Contest.BLOC if True in blocs else Contest.VOIE
            )
            cleaned_data["is_combine"] = False

        # ---------------------------------
        # INTERDICTION : équipe + zone / dégaine
        # ---------------------------------
        if is_team_contest and (has_zone or has_degaine):
            self.add_error(
                None,
                "Un contest par équipe ne peut pas utiliser les zones ou les dégaines."
            )

        # ---------------------------------
        # INTERDICTION : équipe + contest de départ
        # ---------------------------------
        if is_team_contest and initial_contest:
            self.add_error(
                "initial_contest",
                "Un contest par équipe ne peut pas être lié à un contest de départ."
            )

        # ---------------------------------
        # SÉCURITÉ : contest de départ
        # ---------------------------------
        if initial_contest:
            if initial_contest.is_permanent:
                self.add_error(
                    "initial_contest",
                    "Le contest de départ ne peut pas être permanent."
                )

            if not initial_contest.end_date or initial_contest.end_date >= now():
                self.add_error(
                    "initial_contest",
                    "Le contest de départ doit être terminé."
                )

        return cleaned_data
