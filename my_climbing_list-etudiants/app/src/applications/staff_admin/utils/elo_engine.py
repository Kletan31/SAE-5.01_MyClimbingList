# applications/core/utils/elo_engine.py

from collections import defaultdict

from applications.core.models import Seance
from applications.core.utils import cotation_colors

# REGEX pour exclure les voies trop faciles
NIVEAU_PATTERN = r'^[5-9]'

FACTEUR_K = 10
RANKING_REQUIRED_TOPS = 12


# =====================================================
# STRUCTURE D'ÉTAT ELO (persistée côté rebuild)
# =====================================================

def initial_elo_state():
    """
    État minimal nécessaire pour garantir un Elo déterministe.
    """
    return {
        "elo": None,
        "ranking": True,
        "ranking_routes_level": [],
        "echecs_par_voie": defaultdict(int),
        "tentatives_No": 0,
    }


# =====================================================
# API PUBLIQUE
# =====================================================

def compute_day(
    *,
    user,
    bloc,
    day,
    state,
):
    """
    Calcule l'état Elo du jour `day` à partir de l'état J-1.

    Parameters
    ----------
    user : User
    bloc : bool
    day : date
    state : dict
        État Elo issu de J-1 (muté et retourné)

    Returns
    -------
    dict
        Nouvel état Elo
    """

    seances = (
        Seance.objects
        .filter(
            user=user,
            ouverture__bloc=bloc,
            ouverture__niveau__regex=NIVEAU_PATTERN,
            date_seance=day,
        )
        .select_related("ouverture")
        .order_by("created_at")
    )

    for seance in seances:
        _process_seance(seance, state)

    return state


# =====================================================
# LOGIQUE ELO — IDENTIQUE À LA VUE GRAPH
# =====================================================

def _process_seance(seance, state):
    niveau_voie = get_difficulty_rating(seance.ouverture.niveau)

    # ------------------------------
    # Phase de ranking initial
    # ------------------------------
    if state["ranking"]:
        if seance.nb_top or seance.nb_top_lead:
            state["ranking_routes_level"].append(niveau_voie)

        if len(state["ranking_routes_level"]) == RANKING_REQUIRED_TOPS:
            state["elo"] = sum(state["ranking_routes_level"]) / RANKING_REQUIRED_TOPS
            state["ranking"] = False

        return

    ouverture_id = seance.ouverture.id

    # Initialisation du suivi d'échecs
    if ouverture_id not in state["echecs_par_voie"]:
        state["echecs_par_voie"][ouverture_id] = 0

    _adjust_moulinette(seance, niveau_voie, state)
    _adjust_lead(seance, niveau_voie, state)
    _adjust_failures(seance, niveau_voie, ouverture_id, state)


def _adjust_moulinette(seance, niveau_voie, state):
    for i in range(seance.nb_top):
        state["tentatives_No"] += 1
        p = elo_expectation(state["elo"], niveau_voie)
        multiplicateur = 1.5 if i == 0 and seance.flash else 1.0
        gain = FACTEUR_K * (1 - p) * multiplicateur
        state["elo"] += gain


def _adjust_lead(seance, niveau_voie, state):
    for i in range(seance.nb_top_lead):
        state["tentatives_No"] += 1
        p = elo_expectation(state["elo"], niveau_voie)
        multiplicateur = 1.875 if i == 0 and seance.flash_lead else 1.25
        gain = FACTEUR_K * (1 - p) * multiplicateur
        state["elo"] += gain


def _adjust_failures(seance, niveau_voie, ouverture_id, state):
    total_echecs = (
        seance.nb_try + seance.nb_try_lead
        - (seance.nb_top + seance.nb_top_lead)
    )

    for _ in range(total_echecs):
        if state["echecs_par_voie"][ouverture_id] < 3:
            state["tentatives_No"] += 1
            p = elo_expectation(state["elo"], niveau_voie)
            perte = FACTEUR_K * (0 - p)
            state["elo"] += perte
            state["echecs_par_voie"][ouverture_id] += 1


# =====================================================
# OUTILS ELO (STRICTEMENT IDENTIQUES)
# =====================================================

def get_difficulty_rating(niveau):
    facteur = {
        '5a': 1000, '5a+': 1050,
        '5b': 1100, '5b+': 1150,
        '5c': 1200, '5c+': 1250,
        '6a': 1300, '6a+': 1350,
        '6b': 1400, '6b+': 1450,
        '6c': 1500, '6c+': 1550,
        '7a': 1600, '7a+': 1650,
        '7b': 1700, '7b+': 1750,
        '7c': 1800, '7c+': 1850,
        '8a': 1900, '8a+': 1950,
        '8b': 2000, '8b+': 2050,
        '8c': 2100, '8c+': 2150,
        '9a': 2200, '9a+': 2250,
        '9b': 2300, '9b+': 2350,
        '9c': 2400, '9c+': 2450,
    }
    return facteur.get(niveau)


def elo_expectation(niveau_user, niveau_voie):
    return 1 / (1 + 10 ** ((niveau_voie - niveau_user) / 50))


def elo2cotation(valeur):
    niveaux = [
        '5a', '5a+', '5b', '5b+', '5c', '5c+',
        '6a', '6a+', '6b', '6b+', '6c', '6c+',
        '7a', '7a+', '7b', '7b+', '7c', '7c+',
        '8a', '8a+', '8b', '8b+', '8c', '8c+',
        '9a', '9a+', '9b', '9b+', '9c', '9c+',
    ]

    index = int(valeur // 50 - 20) if valeur else -1
    return niveaux[index] if 0 <= index < len(niveaux) else "-"


def elo_to_level_and_color(elo_value):
    level = elo2cotation(elo_value)
    if not level:
        return "-", "#333"

    key = level[0]
    return level, cotation_colors.get(key, "#000000")
