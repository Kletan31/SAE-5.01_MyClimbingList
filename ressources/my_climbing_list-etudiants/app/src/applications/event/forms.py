from django import forms

from applications.core.models import Ouverture

from .models import (
    Event,
    EventPhase,
    EventTeam,
    EventRoute,
)


class EventTeamRegistrationForm(forms.Form):
    participant_1_first_name = forms.CharField(
        max_length=100,
        label="Prénom de la personne 1",
    )

    participant_1_last_name = forms.CharField(
        max_length=100,
        label="Nom de la personne 1",
    )

    participant_1_email = forms.EmailField(
        label="Email de la personne 1",
    )

    participant_1_gender = forms.ChoiceField(
        choices=[
            ("M", "Homme"),
            ("F", "Femme"),
        ],
        label="Catégorie de la personne 1",
    )

    participant_2_first_name = forms.CharField(
        max_length=100,
        label="Prénom de la personne 2",
    )

    participant_2_last_name = forms.CharField(
        max_length=100,
        label="Nom de la personne 2",
    )

    participant_2_email = forms.EmailField(
        label="Email de la personne 2",
    )

    participant_2_gender = forms.ChoiceField(
        choices=[
            ("M", "Homme"),
            ("F", "Femme"),
        ],
        label="Catégorie de la personne 2",
    )

    phase = forms.ModelChoiceField(
        queryset=EventPhase.objects.none(),
        empty_label="Choisir un créneau",
        label="Créneau",
    )

    def __init__(self, *args, event: Event, **kwargs):
        super().__init__(*args, **kwargs)

        self.event = event

        self.fields["phase"].queryset = (
            EventPhase.objects
            .filter(event=event)
            .order_by("start_time")
        )

    def clean_participant_1_email(self):
        return self.cleaned_data["participant_1_email"].strip().lower()

    def clean_participant_2_email(self):
        return self.cleaned_data["participant_2_email"].strip().lower()

    def clean(self):
        cleaned_data = super().clean()

        first_name_1 = cleaned_data.get("participant_1_first_name", "").strip()
        last_name_1 = cleaned_data.get("participant_1_last_name", "").strip()

        first_name_2 = cleaned_data.get("participant_2_first_name", "").strip()
        last_name_2 = cleaned_data.get("participant_2_last_name", "").strip()

        phase = cleaned_data.get("phase")

        if (
            first_name_1
            and last_name_1
            and first_name_2
            and last_name_2
            and first_name_1.lower() == first_name_2.lower()
            and last_name_1.lower() == last_name_2.lower()
        ):
            raise forms.ValidationError(
                "Un duo ne peut pas contenir deux fois la même personne."
            )

        if phase:
            team_count_in_phase = EventTeam.objects.filter(
                phase=phase,
            ).count()

            if team_count_in_phase >= phase.capacity:
                raise forms.ValidationError(
                    "Ce créneau est complet."
                )

        return cleaned_data


class EventTeamEmailUpdateForm(forms.Form):
    participant_1_email = forms.EmailField(
        label="Email de la personne 1",
    )

    participant_2_email = forms.EmailField(
        label="Email de la personne 2",
    )

    def clean_participant_1_email(self):
        return self.cleaned_data["participant_1_email"].strip().lower()

    def clean_participant_2_email(self):
        return self.cleaned_data["participant_2_email"].strip().lower()


class EventRouteForm(forms.ModelForm):
    class Meta:
        model = EventRoute
        fields = [
            "ouverture",
            "has_zone",
            "display_order",
        ]
        labels = {
            "ouverture": "Bloc",
            "has_zone": "Zone présente",
            "display_order": "Ordre d'affichage",
        }

    def __init__(self, *args, event: Event, **kwargs):
        super().__init__(*args, **kwargs)

        self.event = event
        self.instance.event = event

        self.fields["ouverture"].queryset = (
            Ouverture.objects
            .filter(
                salle=event.salle,
                bloc=True,
                active=True,
            )
            .order_by("relais", "niveau", "couleur", "nom")
        )

    def clean_ouverture(self):
        ouverture = self.cleaned_data["ouverture"]

        already_exists = EventRoute.objects.filter(
            event=self.event,
            ouverture=ouverture,
        )

        if self.instance.pk:
            already_exists = already_exists.exclude(pk=self.instance.pk)

        if already_exists.exists():
            raise forms.ValidationError(
                "Ce bloc est déjà associé à l'événement."
            )

        return ouverture

    def clean_display_order(self):
        display_order = self.cleaned_data["display_order"]

        already_exists = EventRoute.objects.filter(
            event=self.event,
            display_order=display_order,
        )

        if self.instance.pk:
            already_exists = already_exists.exclude(pk=self.instance.pk)

        if already_exists.exists():
            raise forms.ValidationError(
                "Cet ordre d'affichage est déjà utilisé pour cet événement."
            )

        return display_order

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.event = self.event

        if commit:
            instance.save()

        return instance


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "date",
        ]
        labels = {
            "name": "Nom",
            "date": "Date de l'événement",
        }
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.date:
            self.initial["date"] = self.instance.date.strftime("%Y-%m-%d")


class EventPhaseForm(forms.ModelForm):
    class Meta:
        model = EventPhase
        fields = [
            "name",
            "start_time",
            "end_time",
            "capacity",
        ]
        labels = {
            "name": "Nom de la phase",
            "start_time": "Heure de début",
            "end_time": "Heure de fin",
            "capacity": "Nombre de places",
        }
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(
                "L’heure de début doit être antérieure à l’heure de fin."
            )

        return cleaned_data