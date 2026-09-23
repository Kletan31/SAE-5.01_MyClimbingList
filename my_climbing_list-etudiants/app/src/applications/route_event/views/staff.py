from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from applications.route_event.decorators import route_event_staff_required
from applications.route_event.models import RouteEvent, RouteEventParticipant
from applications.route_event.permissions import get_staff_event_or_404, get_staff_salle
from applications.route_event.views.public import send_participant_registration_email
from applications.route_event.forms import RouteEventParticipantEmailUpdateForm


@route_event_staff_required
def staff_home(request):
    staff_salle = get_staff_salle(request)

    events = RouteEvent.objects.none()

    if staff_salle:
        events = (
            RouteEvent.objects
            .filter(salle=staff_salle)
            .order_by("-date")
        )

    return render(
        request,
        "route_event/staff/home.html",
        {
            "events": events,
            "staff_salle": staff_salle,
        },
    )


@route_event_staff_required
def staff_participant_list(request, slug):
    event = get_staff_event_or_404(request, slug)

    participants = (
        RouteEventParticipant.objects
        .select_related("phase")
        .filter(event=event)
        .order_by("phase__start_time", "last_name", "first_name")
    )

    return render(
        request,
        "route_event/staff/participant_list.html",
        {
            "event": event,
            "participants": participants,
        },
    )


@route_event_staff_required
def staff_validate_participant(request, participant_id):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related("event"),
        pk=participant_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        participant.is_payment_validated = True
        participant.save(update_fields=["is_payment_validated"])
        return redirect("route_event:staff_participant_list", slug=participant.event.slug)

    return redirect("route_event:staff_participant_list", slug=participant.event.slug)


@route_event_staff_required
def staff_unvalidate_participant(request, participant_id):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related("event"),
        pk=participant_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        participant.is_payment_validated = False
        participant.save(update_fields=["is_payment_validated"])
        return redirect("route_event:staff_participant_list", slug=participant.event.slug)

    return redirect("route_event:staff_participant_list", slug=participant.event.slug)


@route_event_staff_required
def staff_delete_participant(request, participant_id):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related("event"),
        pk=participant_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        event_slug = participant.event.slug
        participant.delete()
        return redirect("route_event:staff_participant_list", slug=event_slug)

    return redirect("route_event:staff_participant_list", slug=participant.event.slug)


@route_event_staff_required
def staff_resend_participant_link(request, participant_id):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related("event", "phase"),
        pk=participant_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        send_participant_registration_email(
            request=request,
            event=participant.event,
            participant=participant,
        )
        return redirect("route_event:staff_participant_list", slug=participant.event.slug)

    return redirect("route_event:staff_participant_list", slug=participant.event.slug)


@route_event_staff_required
def staff_participant_update(request, participant_id):
    participant = get_object_or_404(
        RouteEventParticipant.objects.select_related(
            "event",
            "phase",
        ),
        pk=participant_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        form = RouteEventParticipantEmailUpdateForm(request.POST)

        if form.is_valid():
            participant.email = form.cleaned_data["email"]
            participant.save(update_fields=["email"])

            messages.success(
                request,
                "L’adresse email du participant a bien été mise à jour.",
            )

            return redirect(
                "route_event:staff_participant_list",
                slug=participant.event.slug,
            )
    else:
        form = RouteEventParticipantEmailUpdateForm(
            initial={
                "email": participant.email,
            }
        )

    return render(
        request,
        "route_event/staff/participant_edit.html",
        {
            "event": participant.event,
            "participant": participant,
            "form": form,
        },
    )