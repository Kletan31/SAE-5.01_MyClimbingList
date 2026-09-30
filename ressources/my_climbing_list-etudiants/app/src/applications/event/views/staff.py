from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse

from applications.event.decorators import event_staff_required
from applications.event.models import Event, EventTeam
from applications.event.permissions import get_staff_event_or_404, get_staff_salle
from applications.event.views.public import send_team_registration_emails
from applications.event.forms import EventTeamEmailUpdateForm


def is_ajax_request(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


@event_staff_required
def staff_home(request):
    staff_salle = get_staff_salle(request)

    events = Event.objects.none()

    if staff_salle:
        events = (
            Event.objects
            .filter(salle=staff_salle)
            .order_by("-date")
        )

    return render(
        request,
        "event/staff/home.html",
        {
            "events": events,
            "staff_salle": staff_salle,
        },
    )


@event_staff_required
def staff_team_list(request, slug):
    event = get_staff_event_or_404(request, slug)

    teams = (
        EventTeam.objects
        .select_related(
            "participant_1",
            "participant_2",
            "phase",
        )
        .filter(event=event)
        .order_by("phase__start_time", "created_at")
    )

    return render(
        request,
        "event/staff/team_list.html",
        {
            "event": event,
            "teams": teams,
        },
    )


@event_staff_required
def staff_validate_team(request, team_id):
    team = get_object_or_404(
        EventTeam.objects.select_related("event"),
        pk=team_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        team.is_payment_validated = True
        team.save(update_fields=["is_payment_validated"])

        if is_ajax_request(request):
            return JsonResponse(
                {
                    "success": True,
                    "action": "payment_toggle",
                    "is_payment_validated": True,
                    "payment_label": "Validé",
                    "next_action_url": reverse(
                        "event:staff_unvalidate_team",
                        kwargs={"team_id": team.id},
                    ),
                    "next_action_label": "Mettre en attente",
                }
            )

        return redirect("event:staff_team_list", slug=team.event.slug)

    return redirect("event:staff_team_list", slug=team.event.slug)


@event_staff_required
def staff_unvalidate_team(request, team_id):
    team = get_object_or_404(
        EventTeam.objects.select_related("event"),
        pk=team_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        team.is_payment_validated = False
        team.save(update_fields=["is_payment_validated"])

        if is_ajax_request(request):
            return JsonResponse(
                {
                    "success": True,
                    "action": "payment_toggle",
                    "is_payment_validated": False,
                    "payment_label": "En attente",
                    "next_action_url": reverse(
                        "event:staff_validate_team",
                        kwargs={"team_id": team.id},
                    ),
                    "next_action_label": "Valider",
                }
            )

        return redirect("event:staff_team_list", slug=team.event.slug)

    return redirect("event:staff_team_list", slug=team.event.slug)


@event_staff_required
def staff_delete_team(request, team_id):
    team = get_object_or_404(
        EventTeam.objects.select_related("event"),
        pk=team_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        event_slug = team.event.slug
        team.delete()

        if is_ajax_request(request):
            return JsonResponse(
                {
                    "success": True,
                    "action": "delete",
                }
            )

        return redirect("event:staff_team_list", slug=event_slug)

    return redirect("event:staff_team_list", slug=team.event.slug)


@event_staff_required
def staff_resend_team_link(request, team_id):
    team = get_object_or_404(
        EventTeam.objects.select_related(
            "event",
            "phase",
            "participant_1",
            "participant_2",
        ),
        pk=team_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        send_team_registration_emails(
            request=request,
            event=team.event,
            team=team,
        )

        if is_ajax_request(request):
            return JsonResponse(
                {
                    "success": True,
                    "action": "resend_link",
                    "message": "Lien renvoyé",
                }
            )

        return redirect("event:staff_team_list", slug=team.event.slug)

    return redirect("event:staff_team_list", slug=team.event.slug)


@event_staff_required
def staff_team_update(request, team_id):
    team = get_object_or_404(
        EventTeam.objects.select_related(
            "event",
            "participant_1",
            "participant_2",
            "phase",
        ),
        pk=team_id,
        event__salle=get_staff_salle(request),
    )

    initial_data = {
        "participant_1_email": team.participant_1.email,
        "participant_2_email": team.participant_2.email,
    }

    if request.method == "POST":
        form = EventTeamEmailUpdateForm(request.POST)

        if form.is_valid():
            team.participant_1.email = form.cleaned_data["participant_1_email"]
            team.participant_2.email = form.cleaned_data["participant_2_email"]

            team.participant_1.save(update_fields=["email"])
            team.participant_2.save(update_fields=["email"])

            messages.success(request, "Les adresses email du duo ont bien été mises à jour.")

            return redirect("event:staff_team_list", slug=team.event.slug)
    else:
        form = EventTeamEmailUpdateForm(initial=initial_data)

    return render(
        request,
        "event/staff/team_edit.html",
        {
            "event": team.event,
            "team": team,
            "form": form,
        },
    )