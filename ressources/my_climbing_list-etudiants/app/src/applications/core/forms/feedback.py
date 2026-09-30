from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100, required=True)
    email = forms.EmailField(label="Adresse email", required=True)
    message = forms.CharField(label="Message", widget=forms.Textarea, required=True)
