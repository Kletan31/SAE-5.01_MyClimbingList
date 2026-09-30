from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

from applications.route_event.decorators import route_event_staff_required
from applications.route_event.forms import RouteEventForm, RouteEventPhaseForm
from applications.route_event.models import (
    RouteEvent,
    RouteEventPhase,
    RouteEventParticipant,
    RouteEventPerformance,
    RouteEventRoute,
)
from applications.route_event.permissions import get_staff_event_or_404, get_staff_salle


@route_event_staff_required
def staff_event_list(request):
    staff_salle = get_staff_salle(request)

    events = RouteEvent.objects.none()

    if staff_salle:
        events = (
            RouteEvent.objects
            .select_related("salle")
            .filter(salle=staff_salle)
            .order_by("-date")
        )

    return render(
        request,
        "route_event/staff/event_list.html",
        {
            "events": events,
            "staff_salle": staff_salle,
        },
    )


@route_event_staff_required
def staff_event_create(request):
    staff_salle = get_staff_salle(request)

    if not staff_salle:
        return render(
            request,
            "route_event/staff/event_form.html",
            {
                "form": RouteEventForm(),
                "title": "Créer un événement voie",
                "submit_label": "Créer",
                "error_message": "Votre compte staff n’est associé à aucune salle favorite.",
            },
        )

    if request.method == "POST":
        form = RouteEventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.salle = staff_salle
            event.save()

            return redirect("route_event:staff_event_update", slug=event.slug)
    else:
        form = RouteEventForm()

    return render(
        request,
        "route_event/staff/event_form.html",
        {
            "form": form,
            "title": "Créer un événement voie",
            "submit_label": "Créer",
        },
    )


@route_event_staff_required
def staff_event_update(request, slug):
    event = get_staff_event_or_404(request, slug)

    if request.method == "POST":
        form = RouteEventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save()

            return redirect("route_event:staff_event_update", slug=event.slug)
    else:
        form = RouteEventForm(instance=event)

    phase_form = RouteEventPhaseForm()
    phases = event.phases.all().order_by("start_time")

    return render(
        request,
        "route_event/staff/event_form.html",
        {
            "event": event,
            "form": form,
            "phase_form": phase_form,
            "phases": phases,
            "title": "Modifier un événement voie",
            "submit_label": "Enregistrer",
        },
    )


@route_event_staff_required
@transaction.atomic
def staff_event_delete(request, slug):
    event = get_staff_event_or_404(request, slug)

    if request.method == "POST":

        RouteEventPerformance.objects.filter(
            route__event=event,
        ).delete()

        RouteEventParticipant.objects.filter(
            event=event,
        ).delete()

        RouteEventRoute.objects.filter(
            event=event,
        ).delete()

        RouteEventPhase.objects.filter(
            event=event,
        ).delete()

        event.delete()

        messages.success(
            request,
            "L’événement et toutes ses données associées ont bien été supprimés."
        )

        return redirect("route_event:staff_event_list")

    return render(
        request,
        "route_event/staff/event_confirm_delete.html",
        {
            "event": event,
        },
    )


@route_event_staff_required
def staff_phase_create(request, slug):
    event = get_staff_event_or_404(request, slug)

    if request.method == "POST":
        form = RouteEventPhaseForm(request.POST)

        if form.is_valid():
            phase = form.save(commit=False)
            phase.event = event
            phase.save()

    return redirect("route_event:staff_event_update", slug=event.slug)


@route_event_staff_required
def staff_phase_update(request, phase_id):
    phase = get_object_or_404(
        RouteEventPhase.objects.select_related("event"),
        pk=phase_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        form = RouteEventPhaseForm(request.POST, instance=phase)

        if form.is_valid():
            form.save()
            return redirect("route_event:staff_event_update", slug=phase.event.slug)
    else:
        form = RouteEventPhaseForm(instance=phase)

    return render(
        request,
        "route_event/staff/phase_form.html",
        {
            "event": phase.event,
            "phase": phase,
            "form": form,
            "title": "Modifier une phase",
            "submit_label": "Enregistrer",
        },
    )


@route_event_staff_required
def staff_phase_delete(request, phase_id):
    phase = get_object_or_404(
        RouteEventPhase.objects.select_related("event"),
        pk=phase_id,
        event__salle=get_staff_salle(request),
    )

    event_slug = phase.event.slug

    if request.method == "POST":
        try:
            phase.delete()
            messages.success(request, "La phase a bien été supprimée.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer cette phase : des participants y sont déjà inscrits."
            )

    return redirect("route_event:staff_event_update", slug=event_slug)