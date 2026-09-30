# applications/custom_auth/forms/training.py

from django import forms
from applications.custom_auth.models import Salle


class TrainingAuthorizationForm(forms.Form):
    salles = forms.ModelMultipleChoiceField(
        queryset=Salle.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Salles autorisées"
    )
