from django.contrib import messages
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from applications.route_event.forms import (
    RouteEventParticipantRegistrationForm,
)
from applications.route_event.models import (
    RouteEvent,
    RouteEventParticipant,
)


def route_event_home(request):
    events = (
        RouteEvent.objects
        .prefetch_related("phases")
        .order_by("date")
    )

    event_rows = []

    for event in events:
        total_capacity = sum(
            phase.capacity
            for phase in event.phases.all()
        )

        total_registered = sum(
            phase.participants.count()
            for phase in event.phases.all()
        )

        remaining_places = max(
            total_capacity - total_registered,
            0,
        )

        event_rows.append(
            {
                "event": event,
                "remaining_places": remaining_places,
                "total_capacity": total_capacity,
            }
        )

    return render(
        request,
        "route_event/home.html",
        {
            "event_rows": event_rows,
        },
    )


@transaction.atomic
def route_event_register(request, slug):
    event = get_object_or_404(
        RouteEvent,
        slug=slug,
    )

    if request.method == "POST":
        form = RouteEventParticipantRegistrationForm(
            request.POST,
            event=event,
        )

        if form.is_valid():
            participant = RouteEventParticipant.objects.create(
                event=event,
                phase=form.cleaned_data["phase"],
                first_name=form.cleaned_data["first_name"].strip(),
                last_name=form.cleaned_data["last_name"].strip(),
                email=form.cleaned_data["email"],
                gender=form.cleaned_data["gender"],
            )

            send_participant_registration_email(
                request=request,
                event=event,
                participant=participant,
            )

            messages.success(
                request,
                "Votre inscription a bien été enregistrée. "
                "Un email vous a été envoyé."
            )

            return redirect(
                "route_event:participant_access",
                token=participant.access_token,
            )

    else:
        form = RouteEventParticipantRegistrationForm(
            event=event,
        )

    phases_with_availability = []

    for phase in event.phases.all().order_by("start_time"):
        registered_count = phase.participants.count()

        remaining_places = max(
            phase.capacity - registered_count,
            0,
        )

        phases_with_availability.append(
            {
                "phase": phase,
                "registered_count": registered_count,
                "remaining_places": remaining_places,
            }
        )

    return render(
        request,
        "route_event/register.html",
        {
            "event": event,
            "form": form,
            "phases_with_availability": phases_with_availability,
        },
    )


def send_participant_registration_email(
    request,
    event,
    participant,
):
    access_url = request.build_absolute_uri(
        reverse(
            "route_event:participant_access",
            kwargs={
                "token": participant.access_token,
            },
        )
    )

    subject = (
        f"Inscription enregistrée - {event.name}"
    )

    body = (
        f"Bonjour,\n\n"
        f"Votre inscription pour l’événement "
        f"« {event.name} » a bien été enregistrée.\n\n"
        f"Créneau sélectionné : "
        f"{participant.phase.name}\n"
        f"Participant : "
        f"{participant}\n\n"
        f"Le paiement doit maintenant être validé "
        f"manuellement par le staff.\n"
        f"Tant que cette validation n’a pas eu lieu, "
        f"l’accès au topo et aux résultats reste restreint.\n\n"
        f"Vous pouvez suivre l’état de votre inscription ici :\n"
        f"{access_url}\n\n"
        f"My Climbing List"
    )

    send_mail(
        subject=subject,
        message=body,
        from_email=None,
        recipient_list=[participant.email],
        fail_silently=False,
    )