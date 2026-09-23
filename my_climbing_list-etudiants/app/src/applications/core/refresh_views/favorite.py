# applications/core/refresh_views/favorite.py
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from applications.custom_auth.models import Salle


@csrf_protect
@require_POST
@login_required
def toggle_favorite_salle(request):
    salle_id = request.POST.get("salle_id")
    if not salle_id:
        return HttpResponseBadRequest("Missing salle_id")

    try:
        salle = Salle.objects.get(pk=salle_id)
    except Salle.DoesNotExist:
        return HttpResponseBadRequest("Invalid salle_id")

    profile = request.user.profile
    # Toggle
    if profile.favorite_salle_id == salle.id:
        profile.favorite_salle = None
        profile.save(update_fields=["favorite_salle"])
        return JsonResponse({"status": "unset", "salle_id": salle.id})
    else:
        profile.favorite_salle = salle
        profile.save(update_fields=["favorite_salle"])
        return JsonResponse({"status": "set", "salle_id": salle.id})
