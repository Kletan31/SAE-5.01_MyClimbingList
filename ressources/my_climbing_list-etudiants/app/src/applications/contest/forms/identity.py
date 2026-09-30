# applications/contest/forms/identity.py

from django import forms


class IdentityForm(forms.Form):
    first_name = forms.CharField(label="Prénom", max_length=150)
    last_name = forms.CharField(label="Nom", max_length=150)
    gender = forms.ChoiceField(
        label="Genre",
        choices=[("M", "Masculin"), ("F", "Féminin"), ("N", "Neutre")],
        widget=forms.RadioSelect,
        required=True,
    )

    def clean_first_name(self):
        v = self.cleaned_data["first_name"].strip()
        if not v:
            raise forms.ValidationError("Le prénom est requis.")
        return v

    def clean_last_name(self):
        v = self.cleaned_data["last_name"].strip()
        if not v:
            raise forms.ValidationError("Le nom est requis.")
        return v
