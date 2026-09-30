import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from applications.route_event.models import (
    RouteEvent,
    RouteEventParticipant,
    RouteEventPerformance,
    RouteEventRoute,
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
    help = "Génère des participant·es et performances factices pour tester un événement voie."

    def add_arguments(self, parser):
        parser.add_argument("--slug", required=True)
        parser.add_argument("--participants", type=int, default=40)
        parser.add_argument("--clear", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        slug = options["slug"]
        participant_count = options["participants"]
        clear_existing_data = options["clear"]

        try:
            event = RouteEvent.objects.get(slug=slug)
        except RouteEvent.DoesNotExist as exc:
            raise CommandError(f"Aucun événement voie trouvé avec le slug : {slug}") from exc

        phases = list(event.phases.all().order_by("start_time"))
        routes = list(
            RouteEventRoute.objects
            .filter(event=event)
            .select_related("ouverture")
            .order_by("display_order")
        )

        if not phases:
            raise CommandError("L'événement doit avoir au moins une phase.")

        if not routes:
            raise CommandError("L'événement doit avoir au moins une voie associée.")

        total_capacity = sum(phase.capacity for phase in phases)

        if participant_count > total_capacity:
            raise CommandError(
                f"Impossible de générer {participant_count} participant·es : "
                f"la capacité totale des phases est de {total_capacity}."
            )

        if clear_existing_data:
            self.clear_event_data(event)

        phase_slots = self.build_phase_slots(phases, participant_count)

        created_participants = []
        performances_to_create = []

        for index in range(participant_count):
            phase = phase_slots[index]
            gender = self.pick_gender()

            participant = self.create_participant(
                event=event,
                phase=phase,
                gender=gender,
                participant_index=index + 1,
            )

            created_participants.append(participant)

            performances_to_create.extend(
                self.build_performances_for_participant(
                    participant=participant,
                    routes=routes,
                )
            )

            if (index + 1) % 10 == 0:
                self.stdout.write(f"{index + 1} participant·es préparé·es...")

        RouteEventPerformance.objects.bulk_create(
            performances_to_create,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(created_participants)} participant·es factices généré·es pour « {event.name} »."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(performances_to_create)} performances factices créées."
            )
        )

    def build_phase_slots(self, phases, participant_count):
        phase_slots = []
        phase_index = 0

        while len(phase_slots) < participant_count:
            phase = phases[phase_index % len(phases)]
            current_count = phase_slots.count(phase)

            if current_count < phase.capacity:
                phase_slots.append(phase)

            phase_index += 1

        return phase_slots

    def clear_event_data(self, event):
        RouteEventPerformance.objects.filter(
            participant__event=event,
        ).delete()

        RouteEventParticipant.objects.filter(
            event=event,
        ).delete()

        self.stdout.write(
            self.style.WARNING(
                "Ancien·nes participant·es et performances supprimé·es."
            )
        )

    def pick_gender(self):
        if random.random() < 0.5:
            return RouteEventParticipant.GENDER_MALE

        return RouteEventParticipant.GENDER_FEMALE

    def create_participant(self, event, phase, gender, participant_index):
        if gender == RouteEventParticipant.GENDER_MALE:
            first_name = random.choice(FIRST_NAMES_MALE)
        else:
            first_name = random.choice(FIRST_NAMES_FEMALE)

        last_name = random.choice(LAST_NAMES)

        return RouteEventParticipant.objects.create(
            event=event,
            phase=phase,
            first_name=f"{first_name}{participant_index}",
            last_name=last_name,
            email=f"test-route-{participant_index}@example.com",
            gender=gender,
            is_payment_validated=True,
        )

    def build_performances_for_participant(self, participant, routes):
        participant_strength = random.uniform(0.15, 0.95)
        performances = []

        for route in routes:
            performances.append(
                self.build_performance(
                    participant=participant,
                    route=route,
                    participant_strength=participant_strength,
                )
            )

        return performances

    def build_performance(self, participant, route, participant_strength):
        max_hold = random.randint(25, 45)

        success_probability = 0.10 + (participant_strength * 0.65)
        attempt_probability = 0.45 + (participant_strength * 0.45)

        random_value = random.random()

        if random_value > attempt_probability:
            hold_number = 0
            hold_plus = False

        elif random_value < success_probability:
            hold_number = max_hold
            hold_plus = True

        else:
            min_hold = max(1, int(max_hold * 0.25))
            performance_ratio = random.uniform(
                max(0.15, participant_strength - 0.25),
                min(0.98, participant_strength + 0.25),
            )

            hold_number = max(
                min_hold,
                int(max_hold * performance_ratio),
            )

            hold_plus = random.random() < 0.35

        return RouteEventPerformance(
            participant=participant,
            route=route,
            hold_number=hold_number,
            hold_plus=hold_plus,
        )