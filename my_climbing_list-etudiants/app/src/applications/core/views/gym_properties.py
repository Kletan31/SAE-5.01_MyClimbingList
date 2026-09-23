from applications.core.decorators import non_staff_required
from django.shortcuts import render, get_object_or_404
from applications.core.models import Salle


@non_staff_required
def gym_properties_view(request, salle_id):

    # Récupérer la salle
    salle = get_object_or_404(Salle, id=salle_id)

    # Renvoyer la vue avec le JSON du graphique
    return render(request, "core/gym_properties/gym_properties.html", {
        "salle": salle,
    })
