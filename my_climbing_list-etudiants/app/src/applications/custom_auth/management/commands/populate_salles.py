# applications/custom_auth/management/commands/populate_salles.py

from django.core.management.base import BaseCommand
from applications.custom_auth.models import Salle


class Command(BaseCommand):
    """
    Commande de base pour initialiser les différentes salles du groupe.

    - Chaque salle est associée à un identifiant unique
    - Chaque salle a un ensemble de relais "leadable" qui lui est propre
    """

    def handle(self, *args, **kwargs):
        salle_dict = {
            3: "Montaudran",
            4: "Albi",
            5: "Grabels",
            7: "Saint-Martin",
            9: "Odysseum",
            10: "Marseille",
            12: "Nantes",
            14: "Haut Gazon",
            15: "Perpignan",
            18: "Portet",
            19: "Loisirama",
            20: "Landes",
            100: "Lisboa",
        }

        lead_dict = {
            3: [22, 23, 24, 25, 29, 30, 31, 33, 34, 35, 37, 38, 39, 40, 41, 42, 45, 46],
            4: [18, 19, 20, 21, 22],
            5: [9, 10, 11, 12, 13, 14, 15],
            7: [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            9: [7, 8, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
            10: [3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100],
            12: [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            14: [4, 5, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29, 30, 31, 32, 33, 36],
            15: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            18: [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
            19: [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],
            20: [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41],
            100: [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40],
        }

        for salle_id, nom in salle_dict.items():
            relais = lead_dict.get(salle_id, [])
            salle, created = Salle.objects.update_or_create(
                id=salle_id,
                defaults={'nom': nom, 'relais_en_tete': relais}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Salle {nom} créée avec succès.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Salle {nom} mise à jour avec succès.'))
