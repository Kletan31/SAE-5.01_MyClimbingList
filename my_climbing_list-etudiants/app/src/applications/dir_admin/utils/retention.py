# applications/dir_admin/utils/retention.py

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, DurationField

User = get_user_model()


def get_retention_stats():
    """
    Calcule les statistiques globales de rétention à 1 an :
    - total d'utilisateurs inscrits depuis plus d'un an
    - nombre d'utilisateurs encore actifs un an après leur inscription
    - taux de rétention (en %)
    """
    now = timezone.now()
    one_year = timedelta(days=365)
    one_year_ago = now - one_year

    old_users = User.objects.filter(date_joined__lte=one_year_ago)
    total = old_users.count()

    if total == 0:
        return {
            "rate": None,
            "retained": 0,
            "total": 0,
        }

    retained = (
        old_users
        .filter(last_login__isnull=False)
        .annotate(
            delta=ExpressionWrapper(
                F("last_login") - F("date_joined"),
                output_field=DurationField(),
            )
        )
        .filter(delta__gte=one_year)
        .count()
    )

    rate = round(retained / total * 100, 1)

    return {
        "rate": rate,
        "retained": retained,
        "total": total,
    }
