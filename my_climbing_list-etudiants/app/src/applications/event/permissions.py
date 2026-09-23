from django.shortcuts import get_object_or_404

from applications.event.models import Event


def get_staff_salle(request):
    profile = getattr(request.user, "profile", None)

    if not profile:
        return None

    return profile.favorite_salle


def get_staff_event_or_404(request, slug):
    staff_salle = get_staff_salle(request)

    return get_object_or_404(
        Event,
        slug=slug,
        salle=staff_salle,
    )


def user_can_manage_event(request, event):
    staff_salle = get_staff_salle(request)

    if not staff_salle:
        return False

    return event.salle_id == staff_salle.id