import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from applications.event.models import (
    Event,
    EventParticipant,
    EventPerformance,
    EventRoute,
    EventTeam,
)


FIRST_NAMES_MALE = [
    "Lucas", "Hugo", "Léo", "Nathan", "Louis", "Gabriel", "Jules", "Arthur",
    "Noah", "Raphaël", "Tom", "Ethan", "Maël", "Sacha", "Nolan", "Paul",
]

FIRST_NAMES_FEMALE = [
    "Emma", "Louise", "Alice", "Chloé", "Lina", "Rose", "Léa", "Anna",
    "Mila", "Inès", "Zoé", "Jade", "Manon", "Camille", "Nina", "Sarah",
]

LAST_NAMES = [
    "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand",
    "Dubois", "Moreau", "Laurent", "Simon", "Michel", "Garcia", "Lefevre",
    "Roux", "Fournier", "Girard", "Mercier", "Blanc", "Guerin",
]


class Command(BaseCommand):
    help = "Génère des équipes et performances factices pour tester un événement."

    def add_arguments(self, parser):
        parser.add_argument("--slug", required=True)
        parser.add_argument("--teams", type=int, default=40)
        parser.add_argument("--clear", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        slug = options["slug"]
        team_count = options["teams"]
        clear_existing_data = options["clear"]

        try:
            event = Event.objects.get(slug=slug)
        except Event.DoesNotExist as exc:
            raise CommandError(f"Aucun événement trouvé avec le slug : {slug}") from exc

        phases = list(event.phases.all().order_by("start_time"))
        routes = list(
            EventRoute.objects
            .filter(event=event)
            .select_related("ouverture")
            .order_by("display_order")
        )

        if not phases:
            raise CommandError("L'événement doit avoir au moins une phase.")

        if not routes:
            raise CommandError("L'événement doit avoir au moins un bloc associé.")

        total_capacity = sum(phase.capacity for phase in phases)

        if team_count > total_capacity:
            raise CommandError(
                f"Impossible de générer {team_count} équipes : "
                f"la capacité totale des phases est de {total_capacity}."
            )

        if clear_existing_data:
            self.clear_event_data(event)

        phase_slots = self.build_phase_slots(phases, team_count)

        created_teams = []
        performances_to_create = []

        for index in range(team_count):
            phase = phase_slots[index]
            team_type = self.pick_team_type()

            participant_1, participant_2 = self.create_participants(
                event=event,
                team_index=index + 1,
                team_type=team_type,
            )

            team = EventTeam.objects.create(
                event=event,
                participant_1=participant_1,
                participant_2=participant_2,
                phase=phase,
                is_payment_validated=True,
            )

            created_teams.append(team)

            performances_to_create.extend(
                self.build_performances_for_team(
                    team=team,
                    routes=routes,
                )
            )

            if (index + 1) % 10 == 0:
                self.stdout.write(f"{index + 1} équipes préparées...")

        EventPerformance.objects.bulk_create(
            performances_to_create,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(created_teams)} équipes factices générées pour « {event.name} »."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(performances_to_create)} performances factices créées."
            )
        )

    def build_phase_slots(self, phases, team_count):
        phase_slots = []
        phase_index = 0

        while len(phase_slots) < team_count:
            phase = phases[phase_index % len(phases)]
            current_count = phase_slots.count(phase)

            if current_count < phase.capacity:
                phase_slots.append(phase)

            phase_index += 1

        return phase_slots

    def clear_event_data(self, event):
        participants = EventParticipant.objects.filter(event=event)
        teams = EventTeam.objects.filter(event=event)

        EventPerformance.objects.filter(
            participant__event=event,
        ).delete()

        teams.delete()
        participants.delete()

        self.stdout.write(
            self.style.WARNING(
                "Anciennes équipes, personnes participantes et performances supprimées."
            )
        )

    def pick_team_type(self):
        random_value = random.random()

        if random_value < 0.40:
            return "mixed"

        if random_value < 0.70:
            return "male"

        return "female"

    def create_participants(self, event, team_index, team_type):
        if team_type == "mixed":
            participant_1_gender = EventParticipant.GENDER_MALE
            participant_2_gender = EventParticipant.GENDER_FEMALE
        elif team_type == "male":
            participant_1_gender = EventParticipant.GENDER_MALE
            participant_2_gender = EventParticipant.GENDER_MALE
        else:
            participant_1_gender = EventParticipant.GENDER_FEMALE
            participant_2_gender = EventParticipant.GENDER_FEMALE

        participant_1 = self.create_participant(
            event=event,
            gender=participant_1_gender,
            team_index=team_index,
            participant_number=1,
        )

        participant_2 = self.create_participant(
            event=event,
            gender=participant_2_gender,
            team_index=team_index,
            participant_number=2,
        )

        return participant_1, participant_2

    def create_participant(self, event, gender, team_index, participant_number):
        if gender == EventParticipant.GENDER_MALE:
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)

        last_name = random.choice(LAST_NAMES)

        return EventParticipant.objects.create(
            event=event,
            first_name=f"{first_name}{team_index}",
            last_name=last_name,
            email=f"test-team-{team_index}-{participant_number}@example.com",
            gender=gender,
        )

    def build_performances_for_team(self, team, routes):
        team_strength = random.uniform(0.15, 0.95)
        performances = []

        for route in routes:
            performances.append(
                self.build_performance(
                    participant=team.participant_1,
                    route=route,
                    team_strength=team_strength,
                )
            )

            performances.append(
                self.build_performance(
                    participant=team.participant_2,
                    route=route,
                    team_strength=team_strength,
                )
            )

        return performances

    def build_performance(self, participant, route, team_strength):
        random_value = random.random()

        top_probability = 0.12 + (team_strength * 0.55)
        zone_probability = 0.20 + (team_strength * 0.55)

        top = random_value < top_probability

        if top:
            zone = route.has_zone
        elif route.has_zone:
            zone = random_value < zone_probability
        else:
            zone = False

        return EventPerformance(
            participant=participant,
            route=route,
            top=top,
            zone=zone,
        )