from datetime import date
from django.core.management.base import BaseCommand
from local_demo.lib.seed import seed_demo


class Command(BaseCommand):
    help = 'Crée une seule fois les données fictives locales, sans écraser les exercices.'

    def add_arguments(self, parser):
        parser.add_argument('--reference-date', type=date.fromisoformat,
                            help='Date YYYY-MM-DD pour reproduire exactement les dates du jeu.')

    def handle(self, *args, **options):
        created = seed_demo(options['reference_date'])
        self.stdout.write('Démo créée : 3 salles, 18 ouvertures, 2 grimpeurs, 19 pratiques.'
                          if created else 'Démo déjà initialisée : aucune donnée modifiée.')
