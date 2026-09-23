# applications/core/utils/i18n/month.py

from django.utils.translation import gettext_lazy as _

"""
Abréviations de mois indépendantes de la locale système.
À utiliser pour les graphes (Plotly) et toute UI nécessitant
un contrôle précis de l’i18n.
"""

MONTHS_SHORT = {
    1: _("Janv."),
    2: _("Févr."),
    3: _("Mars"),
    4: _("Avr."),
    5: _("Mai"),
    6: _("Juin"),
    7: _("Juil."),
    8: _("Août"),
    9: _("Sept."),
    10: _("Oct."),
    11: _("Nov."),
    12: _("Déc."),
}
