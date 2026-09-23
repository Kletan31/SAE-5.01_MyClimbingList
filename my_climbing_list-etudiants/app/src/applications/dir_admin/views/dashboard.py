# applications/dir_admin/views/dashboard.py

from django.shortcuts import render
from applications.dir_admin.decorators.superuser_required import superuser_required
from django.utils.timezone import now
from applications.contest.models import Contest
from applications.custom_auth.models import Salle
from django.db.models import Count


@superuser_required
def dashboard_view(request):
    contests = Contest.objects.all().annotate(nb_inscrits=Count("inscriptions"))

    # 🎯 Tri spécial pour contests permanents
    def permanent_sort_key(c):
        if not c.is_permanent:
            return (2, )  # Autres contests en dernier
        discipline_order = {"voie": 0, "bloc": 1}
        niveau_order = {"Intermédiaire": 0, "Confirmé": 1, "Expert": 2, "Mutant": 3}

        # Déduction de la discipline et du niveau via le nom
        discipline = "voie" if "Voie" in c.name else "bloc"
        niveau = next((n for n in niveau_order if n in c.name), None)

        # 🆕 Ajout salle.id comme tri secondaire
        return (
            0,  # Type permanent en premier
            discipline_order.get(discipline, 2),
            niveau_order.get(niveau, 4),
            c.salle.id  # Tri secondaire : salle
        )

    contests = sorted(contests, key=permanent_sort_key)

    salles = Salle.objects.all()

    return render(request, "dir_admin/dashboard/dashboard.html", {
        "contests": contests,
        "now": now(),
        "salles": salles,
    })
