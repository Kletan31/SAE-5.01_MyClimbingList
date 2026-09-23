# applications/contest/utils/scoring.py

from collections import defaultdict
from django.db.models import Q, Count
from django.utils.timezone import now
from typing import Optional

from applications.core.models import Seance
from applications.contest.models import Contest, ContestResult


# =====================================================
# CONDITIONS DE RÉUSSITE (PERMANENT)
# =====================================================
def get_success_q(relais_en_tete: list[int]) -> Q:
    """
    Condition de réussite pour une Seance :
    - voie avec relais en tête imposé  -> top en tête requis
    - bloc ou voie hors 'relais_en_tete' -> top moulinette OU tête
    """
    return (
        Q(ouverture__bloc=False, ouverture__relais__in=relais_en_tete, nb_top_lead__gt=0)
        |
        (
            (Q(ouverture__bloc=True) | ~Q(ouverture__relais__in=relais_en_tete))
            & (Q(nb_top__gt=0) | Q(nb_top_lead__gt=0))
        )
    )


# =====================================================
# PERMANENT — SUCCÈS
# =====================================================
def compute_permanent_success(
    *,
    contest: Contest,
    inscrit_ids: list[int],
    ouverture_ids: list[int],
    relais_en_tete: list[int],
) -> tuple[dict[int, int], dict[int, dict[int, str]]]:
    """
    Calcule pour un contest PERMANENT :
      - counts_by_opening : {ouverture_id: nb_grimpeurs_distincts_ayant_reussi}
      - openings_by_user  : {user_id: {ouverture_id: ouverture_nom}}
    """
    success_q = get_success_q(relais_en_tete)

    seances_qs = (
        Seance.objects
        .filter(
            user_id__in=inscrit_ids,
            ouverture_id__in=ouverture_ids,
            created_at__lte=contest.end_date if contest.end_date else now(),
            ouverture__active=True,
        )
        .filter(success_q)
    )

    # nb grimpeurs distincts par ouverture
    success_counts = (
        seances_qs
        .values("ouverture_id")
        .annotate(total=Count("user", distinct=True))
    )
    counts_by_opening: dict[int, int] = {
        row["ouverture_id"]: row["total"]
        for row in success_counts
    }

    # ouvertures réussies par utilisateur (dédoublées)
    user_opening_rows = (
        seances_qs
        .values("user_id", "ouverture_id", "ouverture__nom")
        .annotate(_n=Count("id"))  # force le group by
    )

    openings_by_user: dict[int, dict[int, str]] = defaultdict(dict)
    for row in user_opening_rows:
        openings_by_user[row["user_id"]][row["ouverture_id"]] = row["ouverture__nom"]

    return counts_by_opening, openings_by_user


# =====================================================
# NON PERMANENT — COMPTAGES
# =====================================================
def compute_non_permanent_counts(contest: Contest) -> dict[int, int]:
    """
    Pour un contest NON-PERMANENT (source = ContestResult),
    renvoie {ouverture_id: nb_grimpeurs_distincts_ayant_reussi}.
    """
    rows = (
        ContestResult.objects
        .filter(contest=contest, has_top=True)
        .values("ouverture_id")
        .annotate(total=Count("user", distinct=True))
    )
    return {r["ouverture_id"]: r["total"] for r in rows}


# =====================================================
# SCORE UTILISATEUR (INTRINSÈQUE AU CONTEST)
# =====================================================
def compute_user_score(*, contest: Contest, user_id: int) -> int:
    """
    Calcule le score intrinsèque d’un utilisateur pour un contest donné,
    SANS score_initial.
    """

    score = 0.0

    if contest.is_permanent:
        ouvertures = list(contest.ouvertures.all())
        ouverture_ids = [o.id for o in ouvertures]

        salle = contest.salle
        relais_en_tete = salle.relais_en_tete if salle and salle.relais_en_tete else []

        counts_by_opening, openings_by_user = compute_permanent_success(
            contest=contest,
            inscrit_ids=[user_id],
            ouverture_ids=ouverture_ids,
            relais_en_tete=relais_en_tete,
        )

        user_openings = openings_by_user.get(user_id, {})

        if contest.format == Contest.CLASSIC:
            score = float(len(user_openings))
        else:
            for oid in user_openings:
                total = counts_by_opening.get(oid, 0)
                if total > 0:
                    score += 1000 / total

    else:
        results = ContestResult.objects.filter(
            contest=contest,
            user_id=user_id,
            has_top=True,
        )

        counts_by_opening = compute_non_permanent_counts(contest)

        for r in results:
            if contest.format == Contest.CLASSIC:
                score += 1
            else:
                total = counts_by_opening.get(r.ouverture_id, 0)
                if total > 0:
                    score += 1000 / total

    return int(score)


# =====================================================
# TOPO
# =====================================================
def build_topo_info(
    *,
    contest: Contest,
    ouvertures: list,
    nb_by_opening: dict[int, int],
) -> list[dict]:
    """
    Construit la liste 'topo' pour le template :
    [{"ouverture": o, "info": "..."}]
    - CLASSIC   : "X grimpeur(s)"
    - 1000 pts  : valeur à la PROCHAINE réussite = 1000/(nb+1)
    """
    topo: list[dict] = []
    for o in ouvertures:
        nb = nb_by_opening.get(o.id, 0)
        if contest.format == Contest.CLASSIC:
            info = f"{nb} grimpeur{'s' if nb != 1 else ''}"
        else:
            potentiel = 1000 / (nb + 1)
            info = f"{int(potentiel)} pts"
        topo.append({"ouverture": o, "info": info})
    return topo


# =====================================================
# RANKING
# =====================================================
def assign_ranks_with_ties(sorted_list, keys=("score", "secondary_score")):
    """
    Attribue des rangs avec gestion classique des ex-aequo.

    - Si plusieurs éléments consécutifs ont les mêmes valeurs pour les clés
      considérées, ils reçoivent le même rang.
    - Le rang suivant tient compte du nombre d'éléments précédents.

    Exemple :
    [10, 9, 9, 9, 8] → [1, 2, 2, 2, 5]

    Paramètres
    ----------
    sorted_list : list[dict]
        Liste déjà triée dans l'ordre du classement.
    keys : str | tuple[str, ...] | list[str]
        Clé ou ensemble de clés utilisées pour déterminer les ex-aequo.

        - Par défaut : ("score", "secondary_score")
        - Si une seule clé est fournie, par exemple "score", alors l'égalité
          est recherchée uniquement sur cette clé.
        - Si une clé n'existe pas sur les éléments, elle vaut None.

    Retour
    ------
    list[int]
        Liste des rangs, dans le même ordre que sorted_list.
    """
    if not sorted_list:
        return []

    # Normalisation de keys pour accepter :
    # - "score"
    # - ("score", "secondary_score")
    # - ["score", "secondary_score"]
    if isinstance(keys, str):
        keys = (keys,)
    else:
        keys = tuple(keys)

    def get_tie_signature(item):
        return tuple(item.get(key) for key in keys)

    ranks = []
    previous_signature = None
    current_rank = 1

    for index, item in enumerate(sorted_list):
        signature = get_tie_signature(item)

        if index == 0:
            current_rank = 1
        elif signature != previous_signature:
            # Rang classique :
            # le rang d'un nouvel élément = sa position (1-based) dans la liste
            current_rank = index + 1

        ranks.append(current_rank)
        previous_signature = signature

    return ranks


# =====================================================
# SCORE ÉQUIPES
# =====================================================
def compute_team_scores(
    *,
    contest: Contest,
    teams,
    results,
    counts_by_opening: dict[int, int],
    current_user_id: Optional[int] = None,
) -> list[dict]:
    """
    Calcule le score des équipes pour un contest.
    """

    team_members = {
        team.id: set(team.members.values_list("id", flat=True))
        for team in teams
    }

    tops_by_opening = defaultdict(set)
    for r in results:
        if r.has_top:
            tops_by_opening[r.ouverture_id].add(r.user_id)

    classement_teams: list[dict] = []

    for team in teams:
        member_ids = team_members.get(team.id, set())
        score = 0.0

        for ouverture_id, all_toppers in tops_by_opening.items():
            team_toppers = all_toppers & member_ids
            n_team = len(team_toppers)

            if n_team == 0:
                continue

            if contest.format == Contest.CLASSIC:
                score += n_team
            else:
                n_opponents = len(all_toppers) - n_team
                score += n_team * (1000 / (n_opponents + 1))

        classement_teams.append({
            "id": team.id,
            "team_name": team.name,
            "score": int(score),
            "is_current_user_team": current_user_id in member_ids,
        })

    return classement_teams
