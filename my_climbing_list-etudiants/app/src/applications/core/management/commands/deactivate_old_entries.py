from datetime import datetime
from django.core.management.base import BaseCommand
from applications.core.models import Ouverture
from applications.core.utils import fetch_csv_data


class Command(BaseCommand):
    help = 'Désactive les entrées qui ne sont plus présentes dans le fichier CSV'

    def handle(self, *args, **kwargs):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("[%Y-%m-%d %H:%M:%S]")

        # Récupération des données CSV
        csv_data = fetch_csv_data('https://topo.example.test/topos.csv')

        if csv_data:
            current_ouverture_ids = self.extract_ouverture_ids_from_csv(csv_data)
            self.deactivate_old_entries(current_ouverture_ids)
            self.stdout.write(self.style.SUCCESS(f'{formatted_datetime} Désactivation des anciennes entrées réussie'))
        else:
            self.stdout.write(self.style.ERROR(f'{formatted_datetime} Échec de la récupération du fichier CSV'))

    @staticmethod
    def extract_ouverture_ids_from_csv(csv_data):
        current_ouverture_ids = set()
        for row in csv_data:
            try:
                ouverture_id = int(row[0])
                current_ouverture_ids.add(ouverture_id)
            except Exception as e:
                print(f'Erreur lors du traitement de la ligne: {row}')
                print(str(e))
        return current_ouverture_ids

    @staticmethod
    def deactivate_old_entries(current_ouverture_ids):
        Ouverture.objects.exclude(id__in=current_ouverture_ids).update(active=False)
