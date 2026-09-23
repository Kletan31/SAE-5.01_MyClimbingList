# applications/contest/views/training.py

from applications.core.decorators import non_staff_required
from django.shortcuts import render, redirect
from django.contrib import messages

from applications.core.forms.training import TrainingAuthorizationForm


# noinspection PyUnresolvedReferences
@non_staff_required
def training_view(request):
    """
    Permet à l'utilisateur de choisir les salles
    autorisées à consulter ses séances pour le suivi d'entraînement.
    """

    profile = request.user.profile

    if request.method == "POST":
        form = TrainingAuthorizationForm(request.POST)

        if form.is_valid():
            salles = form.cleaned_data["salles"]
            profile.authorized_salles.set(salles)
            messages.success(
                request,
                "Les autorisations de suivi d'entraînement ont été mises à jour."
            )
            return redirect("core:training")

    else:
        form = TrainingAuthorizationForm(
            initial={
                "salles": profile.authorized_salles.all()
            }
        )

    context = {
        "form": form,
    }

    return render(
        request,
        "core/training/training.html",
        context,
    )
