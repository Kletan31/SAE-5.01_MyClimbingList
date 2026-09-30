"""Petit jeu fictif : une pratique agrégée par ouverture/utilisateur/date."""
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import CommandError
from django.db import connection, transaction
from django.utils import timezone
from applications.custom_auth.models import Salle, Profile
from applications.core.models import Ouverture, Seance

MARKER = 'mcl-local-demo-v1'
PASSWORD = 'demo-mcl'
# id, salle, bloc, relais/secteur, cotation, nom
ROUTES = [
    (900101, 9001, False, 1, '6a', 'Patience orange'),
    (900102, 9001, False, 2, '6b', 'Cap vers la tête'),
    (900103, 9001, False, 3, '6a+', 'Sommet acquis'),
    (900104, 9001, False, 1, '5a', 'Premier éclair'),
    (900105, 9001, False, 4, '5c', 'Éclair en tête'),
    (900106, 9001, False, 3, '6c', 'Nuage violet'),
    (900107, 9001, False, 4, '7a', 'Horizon neuf'),
    (900108, 9001, False, 5, '5b', 'Souvenir démonté'),
    (900201, 9002, True, 1, '6b', 'Équilibre à trouver'),
    (900202, 9002, True, 2, '5a', 'Bloc éclair'),
    (900203, 9002, True, 3, '6a', 'Traversée acquise'),
    (900204, 9002, True, 1, '5c', 'Pas de velours'),
    (900205, 9002, True, 2, '6c', 'Coordination azur'),
    (900206, 9002, True, 3, '7a', 'Petit satellite'),
    (900301, 9003, False, 1, '5b', 'Passerelle fictive'),
    (900302, 9003, False, 2, '6a', 'Dièdre imaginaire'),
    (900303, 9003, True, 11, '5c', 'Cube citron'),
    (900304, 9003, True, 12, '6b', 'Cube framboise'),
]
# ouverture, jours avant référence, essais/top moulinette ou bloc, essais/top tête,
# flash moulinette/bloc, flash tête. Ordre chronologique pour flash_available.
HISTORY = [
    (900104, 28, 1, 1, 0, 0, True, False),
    (900108, 28, 2, 1, 0, 0, False, False),
    (900101, 21, 3, 0, 0, 0, False, False),
    (900102, 21, 2, 1, 1, 0, False, False),
    (900202, 18, 1, 1, 0, 0, True, False),
    (900201, 18, 3, 0, 0, 0, False, False),
    (900203, 18, 3, 1, 0, 0, False, False),
    (900103, 14, 1, 1, 2, 1, False, False),
    (900105, 14, 0, 0, 1, 1, False, True),
    (900101, 7, 2, 0, 0, 0, False, False),
    (900102, 7, 0, 0, 2, 0, False, False),
    (900204, 5, 2, 1, 0, 0, False, False),
    (900201, 5, 2, 0, 0, 0, False, False),
    (900301, 3, 1, 1, 1, 1, True, True),
    (900303, 3, 2, 1, 0, 0, False, False),
]


def require_local():
    db = settings.DATABASES['default']
    if (os.environ.get('DJANGO_SETTINGS_MODULE') != 'config.settings_local'
            or getattr(settings, 'DJANGO_ENV', None) != 'local'
            or not os.environ.get('MCL_COMPOSE_PROJECT')
            or (db['HOST'], db['NAME'], db['USER']) != ('db', 'mcl_demo', 'mcl_demo')):
        raise CommandError('Seed refusé : destination exclusivement db/mcl_demo en mode local.')


def seed_demo(reference_date=None):
    require_local()  # Avant toute connexion ou écriture.
    anchor = reference_date or timezone.localdate()
    with transaction.atomic():
        # Empêche deux init concurrents de créer la même démo.
        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_advisory_xact_lock(90019003)')
        if Group.objects.filter(name=MARKER).exists():
            return False
        if (Salle.objects.filter(pk__in=[9001, 9002, 9003]).exists()
                or Ouverture.objects.filter(pk__in=[r[0] for r in ROUTES]).exists()
                or User.objects.filter(username__in=['demo.climb', 'demo.climb2']).exists()):
            raise CommandError('IDs/comptes démo déjà occupés sans marqueur : aucune donnée écrasée.')
        for pk, name, lead in [(9001, 'Démo Voie', [2, 3, 4]),
                               (9002, 'Démo Bloc', []), (9003, 'Démo Mixte', [1, 2])]:
            Salle.objects.create(id=pk, nom=name, relais_en_tete=lead)
        colors = [('Orange', '#ee7f00'), ('Bleu', '#2878b5'), ('Vert', '#539b42'),
                  ('Jaune', '#d6b600'), ('Rouge', '#c43d4b'), ('Mauve', '#8b5aa8')]
        for i, (pk, gym, bloc, sector, grade, name) in enumerate(ROUTES):
            color, hex_color = colors[i % len(colors)]
            Ouverture.objects.create(
                id=pk, salle_id=gym, bloc=bloc, relais=sector, niveau=grade,
                nom=name, couleur=color, hex_couleur=hex_color, niveau_couleur=hex_color,
                date_ouverture=anchor-timedelta(days=60), active=pk != 900108,
                ouvreur='Équipe fictive', profil=['dalle', 'vertical', 'dévers'][i % 3],
                style=('coordo' if bloc else 'conti') if i % 2 else 'technic')
        for index, username in enumerate(['demo.climb', 'demo.climb2']):
            user = User.objects.create_user(username, username+'@example.test', PASSWORD)
            profile = Profile.objects.create(user=user, salle_voie_id=9001, salle_bloc_id=9002)
            profile.authorized_salles.set([9001, 9002, 9003])
            seen = set()
            history = HISTORY if index == 0 else [HISTORY[i] for i in (0, 4, 7, 13)]
            for route, days, tries, tops, lead_tries, lead_tops, flash, flash_lead in history:
                Seance.objects.create(
                    user=user, ouverture_id=route, date_seance=anchor-timedelta(days=days),
                    nb_try=tries, nb_top=tops, nb_try_lead=lead_tries, nb_top_lead=lead_tops,
                    flash=flash, flash_lead=flash_lead, flash_available=route not in seen)
                seen.add(route)
        # Groupe sans droits : marqueur persistant, dans la même transaction.
        # Après le premier seed, même les suppressions étudiantes sont conservées.
        Group.objects.create(name=MARKER)
    return True
