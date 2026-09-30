# staff_admin/views/settings.py
from django.shortcuts import render, redirect
from applications.staff_admin.decorators import staff_required
from django.contrib import messages


@staff_required
def salle_settings_view(request):
    user = request.user
    salle = user.profile.salle_voie

    if request.method == "POST":
        value = request.POST.get("masquer_cotation_recentes") == "on"
        salle.masquer_cotation_recentes = value
        salle.save()
        messages.success(request, "Les paramètres ont été enregistrés avec succès.")
        return redirect("staff_admin:settings")

    return render(request, "staff_admin/salle_settings/salle_settings.html", {
        "salle": salle
    })
