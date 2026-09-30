from django.shortcuts import render, redirect
from applications.contest.models import Contest
from django.contrib import messages
from applications.staff_admin.decorators import staff_required


@staff_required
def toggle_permanent_contests_view(request):
    # noinspection PyUnresolvedReferences
    salle = request.user.profile.salle_voie

    # 🔵 On récupère tous les contests permanents de la salle
    contests = Contest.objects.filter(
        salle=salle,
        is_permanent=True
    ).select_related("salle")  # (pas indispensable mais propre)

    # 🛠️ On prépare un ordre manuel
    def sort_key(c):
        discipline_order = 0 if c.discipline == "voie" else 1  # Voie avant Bloc
        niveau_order = {
            "Intermédiaire": 0,
            "Confirmé": 1,
            "Expert": 2,
            "Mutant": 3,
        }.get(c.name.split()[-1], 99)  # On regarde le dernier mot du nom du contest
        return discipline_order, niveau_order

    contests = sorted(contests, key=sort_key)

    if request.method == "POST":
        for contest in contests:
            key = f"enable_{contest.id}"
            contest.is_permanent_enabled = key in request.POST
            contest.save()
        messages.success(request, "Les modifications ont été enregistrées avec succès.")
        return redirect("staff_admin:toggle_permanents")

    return render(request, "staff_admin/permanents/permanents.html", {
        "contests": contests,
    })
