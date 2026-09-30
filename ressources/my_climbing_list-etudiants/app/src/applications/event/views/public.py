import smtplib

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse

from applications.event.forms import EventTeamRegistrationForm
from applications.event.models import Event, EventParticipant, EventTeam


def event_home(request):
    events = (
        Event.objects
        .all()
        .prefetch_related("phases")
        .order_by("date")
    )

    event_rows = []

    for event in events:
        total_capacity = sum(phase.capacity for phase in event.phases.all())
        total_registered = sum(phase.teams.count() for phase in event.phases.all())
        remaining_places = max(total_capacity - total_registered, 0)

        event_rows.append({
            "event": event,
            "remaining_places": remaining_places,
            "total_capacity": total_capacity,
        })

    return render(request, "event/home.html", {"event_rows": event_rows})


def event_register(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if request.method == "POST":
        form = EventTeamRegistrationForm(request.POST, event=event)

        if form.is_valid():
            try:
                with transaction.atomic():
                    participant_1 = EventParticipant.objects.create(
                        event=event,
                        first_name=form.cleaned_data["participant_1_first_name"].strip(),
                        last_name=form.cleaned_data["participant_1_last_name"].strip(),
                        email=form.cleaned_data["participant_1_email"],
                        gender=form.cleaned_data["participant_1_gender"],
                    )

                    participant_2 = EventParticipant.objects.create(
                        event=event,
                        first_name=form.cleaned_data["participant_2_first_name"].strip(),
                        last_name=form.cleaned_data["participant_2_last_name"].strip(),
                        email=form.cleaned_data["participant_2_email"],
                        gender=form.cleaned_data["participant_2_gender"],
                    )

                    team = EventTeam.objects.create(
                        event=event,
                        participant_1=participant_1,
                        participant_2=participant_2,
                        phase=form.cleaned_data["phase"],
                    )

                    send_team_registration_emails(
                        request=request,
                        event=event,
                        team=team,
                    )

            except smtplib.SMTPException:
                form.add_error(
                    None,
                    "L’une des adresses email semble invalide ou a été refusée. "
                    "Merci de vérifier les adresses saisies."
                )
            else:
                messages.success(
                    request,
                    "L’inscription du duo a bien été enregistrée. "
                    "Un email a été envoyé."
                )

                return redirect(
                    "event:team_access",
                    token=team.access_token,
                )

    else:
        form = EventTeamRegistrationForm(event=event)

    phases_with_availability = []

    for phase in event.phases.all().order_by("start_time"):
        registered_count = phase.teams.count()
        remaining_places = max(phase.capacity - registered_count, 0)

        phases_with_availability.append({
            "phase": phase,
            "registered_count": registered_count,
            "remaining_places": remaining_places,
        })

    return render(
        request,
        "event/register.html",
        {
            "event": event,
            "form": form,
            "phases_with_availability": phases_with_availability,
        },
    )


def send_team_registration_emails(request, event, team):
    access_url = request.build_absolute_uri(
        reverse(
            "event:team_access",
            kwargs={"token": team.access_token},
        )
    )

    logo_url = request.build_absolute_uri(static("event/media/logo_salle.svg"))
    big_air_url = request.build_absolute_uri(static("local_demo/salle.svg"))
    info_url = "https://event.example.test"

    subject = f"Inscription enregistrée - {event.name}"

    participants = f"{team.participant_1} / {team.participant_2}"

    phase_start = team.phase.start_time.strftime("%Hh%M")
    phase_end = team.phase.end_time.strftime("%Hh%M")
    phase_label = f"{phase_start} - {phase_end}"

    text_body = (
        "Bonjour,\n\n"
        "Merci pour votre inscription à l’Alteam #3 Big Air Experience.\n\n"
        "Votre équipe est bien enregistrée :\n"
        f"- Créneau : {phase_label}\n"
        f"- Duo : {participants}\n\n"
        "Le règlement se fera directement sur place, le jour de l’événement.\n"
        "La validation de la participation sera effectuée à ce moment-là.\n\n"
        "Conseil pratique :\n"
        "Nous vous recommandons d’arriver environ 30 minutes en avance afin de profiter du lieu, "
        "de vous échauffer et d’être prêt·es pour le début du contest.\n\n"
        "Validation des blocs :\n"
        "Elle se fera via l’application en ligne. Conservez bien le lien ci-dessous "
        "pour accéder à votre espace le jour de l’événement :\n"
        f"{access_url}\n\n"
        "Informations pratiques :\n"
        "Retrouvez toutes les informations ici :\n"
        f"{info_url}\n\n"
        "Nous sommes ravi·es de vous accueillir pour cette édition.\n\n"
        "À bientôt,\n"
        "L’équipe Altissimo Portet"
    )

    html_body = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.5; color: #222;">
        <img src="{logo_url}" alt="Altissimo Portet"
             style="max-width: 100%; width: 220px; height: auto;">

        <p>Bonjour,</p>

        <p>
            Merci pour votre inscription à
            <strong>l’Alteam #3 Big Air Experience</strong>.
        </p>

        <p>Votre équipe est bien enregistrée :</p>

        <ul>
            <li><strong>Créneau :</strong> {phase_label}</li>
            <li><strong>Duo :</strong> {participants}</li>
        </ul>

        <p>
            Le règlement se fera directement sur place, le jour de l’événement.<br>
            La validation de la participation sera effectuée à ce moment-là.
        </p>

        <p>
            <strong>Conseil pratique :</strong><br>
            Nous vous recommandons d’arriver environ 30 minutes en avance afin de profiter du lieu,
            de vous échauffer et d’être prêt·es pour le début du contest.
        </p>

        <p>
            <strong>Validation des blocs :</strong><br>
            Elle se fera via l’application en ligne. Conservez bien le lien ci-dessous
            pour accéder à votre espace le jour de l’événement :<br>

            <a href="{access_url}" style="color: #0057ff; text-decoration: none;">
                Accéder à l’espace d’inscription
            </a>
        </p>

        <p style="margin-top: 1em">
            <strong>Informations pratiques :</strong><br>
            Retrouvez toutes les informations ici :<br>

            <a href="{info_url}" style="color: #0057ff; text-decoration: none;">
                Voir les informations pratiques
            </a>
        </p>

        <p style="margin-top: 1em">
            Nous sommes ravi·es de vous accueillir pour cette édition.
        </p>

        <p>
            À bientôt,<br>
            L’équipe Altissimo Portet
        </p>

        <img src="{big_air_url}" alt="Alteam Big Air Experience"
             style="max-width: 100%; width: 400px; height: auto;">
    </div>
    """

    recipients = list({
        team.participant_1.email.strip().lower(),
        team.participant_2.email.strip().lower(),
    })

    recipients = [
        email
        for email in recipients
        if email
    ]

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,
        to=recipients,
    )

    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)