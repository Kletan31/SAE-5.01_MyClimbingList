# applications/contest/management/commands/generate_permanent_contests.py

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from applications.contest.models import Contest
from applications.core.models import Ouverture
from applications.custom_auth.models import Salle


class Command(BaseCommand):
    help = "Génère automatiquement les contests permanents (voie/bloc et par niveau) pour chaque salle."

    NIVEAUX = {
        "Intermédiaire": ["5a", "5a+", "5b", "5b+", "5c", "5c+"],
        "Confirmé": ["6a", "6a+", "6b", "6b+", "6c", "6c+"],
        "Expert": ["7a", "7a+", "7b", "7b+", "7c", "7c+"],
        "Mutant": ["8a", "8a+", "8b", "8b+", "8c", "8c+", "9a", "9a+", "9b", "9b+", "9c", "9c+"]
    }

    DISCIPLINES = [Contest.BLOC, Contest.VOIE]

    def handle(self, *args, **kwargs):
        for salle in Salle.objects.all():
            for discipline in self.DISCIPLINES:
                for niveau_nom, niveaux in self.NIVEAUX.items():
                    name = f"{discipline.capitalize()} {niveau_nom}"

                    contest, created = Contest.objects.get_or_create(
                        salle=salle,
                        name=name,
                        is_permanent=True,
                        defaults={
                            'description': f"Contest permanent {discipline} niveau {niveau_nom}",
                            'discipline': discipline,
                            'format': Contest.POINTS_1000,
                            'start_date': now(),
                            'end_date': None,
                            'created_by': None,
                            'is_active': True,
                            'is_payant': False,
                            'is_permanent_enabled': False,
                        }
                    )

                    # Sélectionner les ouvertures valides
                    ouvertures = Ouverture.objects.filter(
                        salle=salle,
                        bloc=(discipline == Contest.BLOC),
                        niveau__in=niveaux,
                        active=True
                    )

                    if not ouvertures.exists():
                        self.stdout.write(self.style.NOTICE(f"Aucune ouverture pour {name} à {salle}"))

                    # Toujours mettre à jour les ouvertures
                    # noinspection PyUnresolvedReferences
                    contest.ouvertures.set(ouvertures)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Créé : {name} à {salle}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Mise à jour : {name} à {salle}"))
