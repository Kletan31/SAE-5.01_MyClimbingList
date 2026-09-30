# applications/core/utils/i18n/normalize.py

import unicodedata


def nfc(value):
    """
    Normalise une chaîne Unicode en NFC.

    Indispensable avant toute traduction gettext,
    notamment sur macOS où les chaînes peuvent être en NFD
    (caractères accentués décomposés).

    :param value: str ou autre
    :return: str normalisée NFC ou valeur inchangée
    """
    if not isinstance(value, str):
        return value
    return unicodedata.normalize("NFC", value)
