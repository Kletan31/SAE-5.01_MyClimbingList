from django.db.models import Q, Sum, Min, Exists, OuterRef
from applications.core.models import Seance, Salle

# REGEX pour exclure les voies "découvertes"
niveau_pattern = r'^[3-9]'


def get_routes_data(user, bloc, flashed, leaded):
    # Logique du queryset
    logbook = (
        Seance.objects.filter(
            user=user,
            ouverture__bloc=bloc,
            ouverture__niveau__regex=niveau_pattern
        )
        .values(
            'ouverture_id',
            'ouverture__salle__nom',
            'ouverture__niveau',
            'ouverture__niveau_couleur',
            'ouverture__profil',
            'ouverture__style',
            'ouverture__nom',
            'ouverture__relais',
            'ouverture__couleur',
        )  # Grouper par ouverture
        .annotate(
            total_top=Sum('nb_top'),  # Total des tops pour chaque ouverture_id
            total_top_lead=Sum('nb_top_lead'),  # Total des tops lead pour chaque ouverture_id
            total_try=Sum('nb_try'),  # Total des try pour chaque ouverture_id
            total_try_lead=Sum('nb_try_lead'),  # Total des try lead pour chaque ouverture_id
            first_top_date=Min(  # Première date de succès (top ou top lead)
                'date_seance',
                filter=Q(nb_top__gt=0) | Q(nb_top_lead__gt=0),
            ),
            leaded=Exists(  # Indicateur booléen pour les ouvertures en tête
                Seance.objects.filter(
                    Q(nb_top_lead__gt=0),
                    ouverture_id=OuterRef('ouverture_id'),
                    user=user,
                )
            ),
            flashed=Exists(  # Indicateur booléen pour les ouvertures flashées
                Seance.objects.filter(
                    Q(flash=True) | Q(flash_lead=True),
                    ouverture_id=OuterRef('ouverture_id'),
                    user=user,
                )
            ),
        )
        .filter(Q(total_top__gt=0) | Q(total_top_lead__gt=0))  # Garder seulement les ouvertures accomplies
        .order_by('-ouverture__niveau')  # Trier par niveau (les plus difficiles en haut)
    )

    # Logique conditionnelle pour combiner les filtres
    if flashed and leaded:
        logbook = logbook.filter(flashed=True, leaded=True)
    elif flashed:
        logbook = logbook.filter(flashed=True)
    elif leaded:
        logbook = logbook.filter(leaded=True)

    # Ajouter la clé 'leadable'
    logbook = list(logbook)
    for entry in logbook:
        relais = entry['ouverture__relais']
        salle_nom = entry['ouverture__salle__nom']
        salle = Salle.objects.get(nom=salle_nom)
        entry['leadable'] = relais in salle.relais_en_tete

    # Retourner les données
    return logbook
