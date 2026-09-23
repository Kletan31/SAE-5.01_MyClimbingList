from django.core.management.base import BaseCommand
from applications.core.models import Ouverture


class Command(BaseCommand):
    help = 'Supprime toutes les entrées de la table Ouverture'

    def handle(self, *args, **kwargs):
        Ouverture.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Toutes les entrées de la table Ouverture ont été supprimées.'))
