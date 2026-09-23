# applications/contest/utils/participant_detail_core.py

from collections import defaultdict
from django.utils.timezone import now
from django.shortcuts import render

from applications.contest.models import Contest, Inscription, ContestResult
from applications.core.models import Seance


def participant_detail_core(
    *,
    request,
    contest: Contest,
    membres,
    participant,
    is_team: bool,
):
    """
    Logique centrale pour l’affichage du détail :
    - d’un grimpeur (is_team=False)
    - ou d’une équipe (is_team=True)

    membres = iterable de User
    participant = User ou Team
    """

    # =====================================================
    # INSCRITS ACTIFS
    # =====================================================
    base_inscriptions = Inscription.objects.filter(contest=contest)

    if contest.is_payant:
        actifs_qs = base_inscriptions.filter(status=Inscription.Status.ACCEPTED)
    else:
        actifs_qs = base_inscriptions.exclude(status=Inscription.Status.REFUSED)

    inscrits_ids = set(actifs_qs.values_list("user", flat=True))
    member_ids = {u.id for u in membres}

    resultats = []
    total_score = 0

    # =====================================================
    # SCORE INITIAL (héritage)
    # =====================================================
    score_initial = 0

    # Le score initial n’a de sens que pour un participant individuel
    if not is_team:
        inscription = (
            Inscription.objects
            .filter(contest=contest, user=participant)
            .first()
        )
        if inscription and inscription.score_initial is not None:
            score_initial = inscription.score_initial

    # =====================================================
    # CONTEST PERMANENT
    # =====================================================
    if contest.is_permanent:
        ouvertures = contest.ouvertures.all().select_related("salle")
        salle = contest.salle
        relais_en_tete = salle.relais_en_tete if salle else []

        # Séances des membres (pour afficher le détail)
        seances_membres = (
            Seance.objects
            .filter(
                user__in=membres,
                ouverture__in=ouvertures,
                created_at__lte=contest.end_date if contest.end_date else now(),
            )
            .select_related("ouverture")
            .distinct()
        )

        # Pour 1000 points : tous les toppers par ouverture
        toppers_by_opening = defaultdict(set)

        if contest.format != Contest.CLASSIC:
            all_seances = (
                Seance.objects
                .filter(
                    user_id__in=inscrits_ids,
                    ouverture__in=ouvertures,
                    created_at__lte=contest.end_date if contest.end_date else now(),
                    ouverture__active=True,
                )
                .select_related("ouverture")
            )

            for s in all_seances:
                o = s.ouverture
                if not o:
                    continue

                if not o.bloc and o.relais in relais_en_tete:
                    success = (s.nb_top_lead or 0) > 0
                else:
                    success = ((s.nb_top or 0) > 0) or ((s.nb_top_lead or 0) > 0)

                if success:
                    toppers_by_opening[o.id].add(s.user_id)

        seen = set()

        for s in seances_membres:
            o = s.ouverture
            if not o or o.id in seen:
                continue

            if not o.bloc and o.relais in relais_en_tete:
                success = (s.nb_top_lead or 0) > 0
            else:
                success = ((s.nb_top or 0) > 0) or ((s.nb_top_lead or 0) > 0)

            if not success:
                continue

            seen.add(o.id)

            # --- calcul points ---
            if contest.format == Contest.CLASSIC:
                pts = 1
            else:
                all_toppers = toppers_by_opening.get(o.id, set())

                if is_team:
                    n_team = len(all_toppers & member_ids)
                    if n_team == 0:
                        continue
                    n_opponents = len(all_toppers - member_ids)
                    pts = n_team * (1000 / (n_opponents + 1))
                else:
                    total = len(all_toppers)
                    pts = 1000 / total if total > 0 else 0

            resultats.append({
                "ouverture": o,
                "points": int(pts),
                "has_top": True,
                "has_zone": None,
                "degaines_reached": None,
            })

            total_score += pts

    # =====================================================
    # CONTEST NON PERMANENT
    # =====================================================
    else:
        results = (
            ContestResult.objects
            .filter(contest=contest, user__in=membres)
            .select_related("ouverture")
        )

        toppers_by_opening = defaultdict(set)

        if contest.format != Contest.CLASSIC:
            for oid, uid in (
                ContestResult.objects
                .filter(contest=contest, has_top=True)
                .values_list("ouverture_id", "user_id")
            ):
                toppers_by_opening[oid].add(uid)

        seen = set()

        for r in results:
            if r.ouverture_id in seen:
                continue

            if not (r.has_top or r.has_zone or r.degaines_reached):
                continue

            seen.add(r.ouverture_id)

            if contest.format == Contest.CLASSIC:
                pts = 1 if r.has_top else 0
            else:
                if not r.has_top:
                    pts = 0
                else:
                    all_toppers = toppers_by_opening.get(r.ouverture_id, set())

                    if is_team:
                        n_team = len(all_toppers & member_ids)
                        if n_team == 0:
                            continue
                        n_opponents = len(all_toppers - member_ids)
                        pts = n_team * (1000 / (n_opponents + 1))
                    else:
                        total = len(all_toppers)
                        pts = 1000 / total if total > 0 else 0

            resultats.append({
                "ouverture": r.ouverture,
                "points": int(pts),
                "has_top": r.has_top,
                "has_zone": r.has_zone,
                "degaines_reached": r.degaines_reached,
            })

            total_score += pts

    # =====================================================
    # RENDER
    # =====================================================
    return render(
        request,
        "contest/participant_detail/participant_detail.html",
        {
            "participant": participant,
            "contest": contest,
            "resultats": resultats,
            "total_score": int(total_score),
            "score_initial": int(score_initial),
            "is_team": is_team,
        },
    )
