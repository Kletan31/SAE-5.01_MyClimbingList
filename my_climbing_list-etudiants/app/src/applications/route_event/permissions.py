from django.shortcuts import get_object_or_404

from applications.route_event.models import RouteEvent


def get_staff_salle(request):
    profile = getattr(request.user, "profile", None)

    if not profile:
        return None

    return profile.favorite_salle


def get_staff_event_or_404(request, slug):
    staff_salle = get_staff_salle(request)

    return get_object_or_404(
        RouteEvent,
        slug=slug,
        salle=staff_salle,
    )