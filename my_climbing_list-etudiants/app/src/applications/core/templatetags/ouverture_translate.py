# applications/core/templatetags/ouverture_translate.py

from django import template
from django.utils.translation import gettext as _

register = template.Library()


# ============================
# Mappings FR (langue source)
# ============================

PROFILE_MAP = {
    "dalle": "dalle",
    "vertical": "vertical",
    "dévers": "dévers",
    "dièdre": "dièdre",
    "toit": "toit",
}

STYLE_MAP = {
    "bloc": "bloc",
    "classic": "classic",
    "conti": "conti",
    "coordo": "coordo",
    "physic": "physic",
    "rési": "rési",
    "technic": "technic",
    "tricky": "tricky",
}

COLOR_MAP = {
    "Blanc": "Blanc",
    "Bleu": "Bleu",
    "Bois": "Bois",
    "Gris": "Gris",
    "Jaune": "Jaune",
    "Marron": "Marron",
    "Mauve": "Mauve",
    "Noir": "Noir",
    "Orange": "Orange",
    "Rose": "Rose",
    "Rouge": "Rouge",
    "Vert": "Vert",
}


# ============================
# Filtres template
# ============================

@register.filter
def ouverture_profile(value):
    """
    Traduit le profil d'une ouverture.
    """
    label = PROFILE_MAP.get(value)
    return _(label) if label else value


@register.filter
def ouverture_style(value):
    """
    Traduit le style d'une ouverture.
    """
    label = STYLE_MAP.get(value)
    return _(label) if label else value


@register.filter
def ouverture_color(value):
    """
    Traduit la couleur des prises.
    """
    label = COLOR_MAP.get(value)
    return _(label) if label else value
