# applications/contest/views/home.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce

from applications.contest.models import Contest
from applications.contest.utils import get_salles_ordered_by_user_activity
from applications.contest.forms import IdentityForm
from applications.custom_auth.models import Profile


@login_required
def contest_home_view(request):
    user = request.user

    # S'assurer qu'on a un profile (et donc un champ gender)
    profile, _ = Profile.objects.get_or_create(user=user)

    # Afficher le modal si prénom/nom manquent OU si le genre n'a pas été choisi (profile.gender == "")
    needs_identity = (not user.first_name) or (not user.last_name) or (not profile.gender)

    if request.method == "POST" and "update_identity" in request.POST:
        form = IdentityForm(request.POST)
        if form.is_valid():
            # Nom/Prénom
            user.first_name = form.cleaned_data["first_name"].strip()
            user.last_name = form.cleaned_data["last_name"].strip()
            user.save(update_fields=["first_name", "last_name"])

            # Genre (forcé à M/F/N — action explicite de l'utilisateur via le form requis)
            profile.gender = form.cleaned_data["gender"]
            profile.save(update_fields=["gender"])

            messages.success(request, "Profil mis à jour. Merci !")
            return redirect("contest:home")
    else:
        # Si le profil n'a jamais choisi (""), on ne pré-sélectionne rien pour forcer une action utilisateur
        initial_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        if profile.gender in ("M", "F", "N"):
            initial_data["gender"] = profile.gender
        # Sinon, on laisse le champ sans valeur initiale

        form = IdentityForm(initial=initial_data)

    # Salles déjà triées par activité utilisateur
    salles = get_salles_ordered_by_user_activity(user)

    # Annotations contests en cours / à venir (non-permanents)
    now_ = now()

    contests_running_subq = (
        Contest.objects.filter(
            salle=OuterRef("pk"),
            is_active=True,
            is_permanent=False,
            start_date__lte=now_,
            end_date__gte=now_,
        )
        .values("salle")
        .annotate(c=Count("id"))
        .values("c")[:1]
    )

    contests_upcoming_subq = (
        Contest.objects.filter(
            salle=OuterRef("pk"),
            is_active=True,
            is_permanent=False,
            start_date__gt=now_,   # à venir
        )
        .values("salle")
        .annotate(c=Count("id"))
        .values("c")[:1]
    )

    salles = salles.annotate(
        active_contests=Coalesce(Subquery(contests_running_subq), 0, output_field=IntegerField()),
        upcoming_contests=Coalesce(Subquery(contests_upcoming_subq), 0, output_field=IntegerField()),
    )

    return render(request, "contest/home/home.html", {
        "salles": salles,
        "needs_identity": needs_identity,
        "identity_form": form,
    })
