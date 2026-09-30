from django import forms

from applications.core.models import Ouverture

from .models import (
    RouteEvent,
    RouteEventPhase,
    RouteEventParticipant,
    RouteEventRoute,
)


class RouteEventForm(forms.ModelForm):
    class Meta:
        model = RouteEvent
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


class RouteEventPhaseForm(forms.ModelForm):
    class Meta:
        model = RouteEventPhase
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


class RouteEventRouteForm(forms.ModelForm):
    class Meta:
        model = RouteEventRoute
        fields = [
            "ouverture",
            "display_order",
        ]
        labels = {
            "ouverture": "Voie",
            "display_order": "Ordre d'affichage",
        }

    def __init__(self, *args, event: RouteEvent, **kwargs):
        super().__init__(*args, **kwargs)

        self.event = event
        self.instance.event = event

        self.fields["ouverture"].queryset = (
            Ouverture.objects
            .filter(
                salle=event.salle,
                bloc=False,
                active=True,
            )
            .order_by("relais", "niveau", "couleur", "nom")
        )

    def clean_ouverture(self):
        ouverture = self.cleaned_data["ouverture"]

        already_exists = RouteEventRoute.objects.filter(
            event=self.event,
            ouverture=ouverture,
        )

        if self.instance.pk:
            already_exists = already_exists.exclude(pk=self.instance.pk)

        if already_exists.exists():
            raise forms.ValidationError(
                "Cette voie est déjà associée à l'événement."
            )

        return ouverture

    def clean_display_order(self):
        display_order = self.cleaned_data["display_order"]

        already_exists = RouteEventRoute.objects.filter(
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

class RouteEventParticipantRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="Prénom")
    last_name = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email")
    gender = forms.ChoiceField(
        choices=[
            ("M", "Homme"),
            ("F", "Femme"),
        ],
        label="Catégorie",
    )

    phase = forms.ModelChoiceField(
        queryset=RouteEventPhase.objects.none(),
        empty_label="Choisir un créneau",
        label="Créneau",
    )

    def __init__(self, *args, event: RouteEvent, **kwargs):
        super().__init__(*args, **kwargs)

        self.event = event
        self.fields["phase"].queryset = (
            RouteEventPhase.objects
            .filter(event=event)
            .order_by("start_time")
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        already_exists = RouteEventParticipant.objects.filter(
            event=self.event,
            email=email,
        ).exists()

        if already_exists:
            raise forms.ValidationError(
                "Cette adresse email est déjà inscrite à cet événement."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        phase = cleaned_data.get("phase")

        if phase:
            registered_count = phase.participants.count()

            if registered_count >= phase.capacity:
                raise forms.ValidationError("Ce créneau est complet.")

        return cleaned_data

    
class RouteEventParticipantEmailUpdateForm(forms.Form):
    email = forms.EmailField(
        label="Email",
    )

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()