# applications/contest/utils/get_salles_ordered.py

from django.db.models import Sum, F, OuterRef, Subquery, IntegerField
from django.db.models.functions import Coalesce
from applications.custom_auth.models import Salle
from applications.core.models import Seance

NIVEAU_PATTERN = r'^[5-9]'


def get_salles_ordered_by_user_activity(user):
    """
    Retourne un QuerySet de Salle ordonné par l'activité de l'utilisateur
    (somme nb_try + nb_try_lead sur ouvertures actives et niveau >=5), décroissant.
    En cas d'égalité, tri alpha sur le nom.
    """
    seances_per_salle = (
        Seance.objects
        .filter(
            user=user,
            ouverture__salle=OuterRef("pk"),
            ouverture__active=True,
            ouverture__niveau__regex=NIVEAU_PATTERN,
        )
        .values("ouverture__salle")
        .annotate(total=Coalesce(Sum(F("nb_try") + F("nb_try_lead")), 0, output_field=IntegerField()))
        .values("total")[:1]
    )

    return (
        Salle.objects
        .annotate(total_user_try=Coalesce(Subquery(seances_per_salle), 0))
        .order_by("-total_user_try", "nom")
    )
