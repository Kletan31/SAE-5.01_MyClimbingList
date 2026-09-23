# applications/core/views/profil.py

from django.shortcuts import render
from applications.core.decorators import non_staff_required


@non_staff_required
def profile_view(request):
    user = request.user
    bloc = request.GET.get('bloc', 'false').lower() == 'true'

    profile = getattr(user, "profile", None)

    if profile:
        salle_voie_display = profile.favorite_salle or profile.salle_voie
        salle_bloc_display = profile.favorite_salle or profile.salle_bloc
    else:
        salle_voie_display = None
        salle_bloc_display = None

    return render(
        request,
        'core/profile/profile.html',
        {
            'user': user,
            'bloc': bloc,
            'salle_voie_display': salle_voie_display or "-",
            'salle_bloc_display': salle_bloc_display or "-",
        }
    )
