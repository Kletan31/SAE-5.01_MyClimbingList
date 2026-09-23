# applications/core/templatetags/core_extras.py
import unicodedata
from django import template

register = template.Library()


def _normalize(s):
    """Supprime les accents et met en minuscule."""
    if not isinstance(s, str):
        return s
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    ).lower()


# =========================
#  Filtres utilitaires
# =========================

@register.filter
def split(value, delimiter=","):
    """
    Permet de séparer une chaîne de caractères en liste.
    Exemple : "a,b,c"|split:"," → ["a", "b", "c"]
    """
    if not value:
        return []
    return [v.strip() for v in value.split(delimiter)]


@register.filter
def get_item(dictionary, key):
    """
    Retourne la valeur associée à 'key' dans un dictionnaire,
    en ignorant les accents et la casse.
    """
    if not isinstance(dictionary, dict):
        return ""
    norm_key = _normalize(key)
    for k, v in dictionary.items():
        if _normalize(k) == norm_key:
            return v
    return ""


@register.filter
def split_pair(value, sep=":"):
    """Sépare une chaîne 'a:b' en tuple ('a', 'b')"""
    parts = value.split(sep, 1)
    return parts if len(parts) == 2 else (value, "")
