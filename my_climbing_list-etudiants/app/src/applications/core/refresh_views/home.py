from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from applications.core.utils import aggregate_seances_data, get_user_seances


@login_required
@require_GET
def load_more_sessions(request):
    """
    Vue API : charge 10 séances supplémentaires et renvoie le HTML rendu.
    """
    user = request.user
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 10))

    seances = get_user_seances(user)
    seances_data = aggregate_seances_data(seances, offset=offset, limit=limit)

    # Rendre le fragment HTML avec les variables nécessaires
    html = render_to_string(
        "core/home/_sessions_fragment.html",
        {"seances_data": seances_data},
        request=request,  # nécessaire pour la traduction et le contexte utilisateur
    )

    return HttpResponse(html)
