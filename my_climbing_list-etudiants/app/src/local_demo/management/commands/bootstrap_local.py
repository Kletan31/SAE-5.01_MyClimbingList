from django.conf import settings
from django.core.management import BaseCommand, call_command, CommandError


class Command(BaseCommand):
    help = "Prépare uniquement la base PostgreSQL jetable mcl-local."

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        if settings.DJANGO_ENV != "local" or (db["HOST"], db["NAME"]) != ("db", "mcl_demo"):
            raise CommandError("Destination locale incorrecte ; aucune opération effectuée")
        self.stdout.write("mcl-local : host=db port=5432 database=mcl_demo ; migrations natives puis syncdb local")
        # syncdb crée les clés étrangères avant les migrations : auth_user doit
        # déjà exister pour Profile.user et les autres relations vers User.
        call_command("migrate", interactive=False)
        call_command("migrate", run_syncdb=True, interactive=False)
        call_command("seed_demo")
