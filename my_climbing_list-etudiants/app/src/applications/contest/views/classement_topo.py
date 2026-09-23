# applications/contest/views/classement_topo.py

from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from applications.contest.models import Contest, Inscription, ContestResult, Team
from applications.custom_auth.models import Profile
from applications.contest.utils import extract_natural_key
from applications.contest.utils.scoring import (
    compute_permanent_success,
    compute_non_permanent_counts,
    build_topo_info,
    assign_ranks_with_ties,
    compute_team_scores,
)
from applications.contest.utils.score_initialization import initialize_score_initial


@login_required
def classement_topo_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    salle = contest.salle
    relais_en_tete = salle.relais_en_tete if salle and salle.relais_en_tete else []

    # =====================================================
    # PARTICIPANTS
    # =====================================================
    if contest.is_team_contest:
        participant_ids = list(
            Team.objects
            .filter(contest=contest)
            .values_list("members__id", flat=True)
            .distinct()
        )
    else:
        inscrits = Inscription.objects.filter(contest=contest)
        if contest.is_payant:
            inscrits = inscrits.filter(status=Inscription.Status.ACCEPTED)
        else:
            inscrits = inscrits.exclude(status=Inscription.Status.REFUSED)
        participant_ids = list(inscrits.values_list("user_id", flat=True))

    # =====================================================
    # INSCRIPTIONS (pour score_initial)
    # =====================================================
    inscriptions = (
        Inscription.objects
        .filter(contest=contest, user_id__in=participant_ids)
    )
    inscription_by_user = {i.user_id: i for i in inscriptions}

    # =====================================================
    # TRI DES OUVERTURES
    # =====================================================
    ouvertures = list(contest.ouvertures.all())
    if contest.sort_by_name:
        ouvertures = sorted(ouvertures, key=lambda o: extract_natural_key(o.nom))
    else:
        ouvertures = sorted(ouvertures, key=lambda o: (0 if o.bloc else 1, o.relais or 0))

    ouverture_ids = [o.id for o in ouvertures]

    # =====================================================
    # DONNÉES UTILISATEURS
    # =====================================================
    profils = Profile.objects.filter(user_id__in=participant_ids)
    genre_map = {p.user_id: p.gender for p in profils}

    usernames = {
        int(uid): uname
        for uid, uname in (
            request.user.__class__.objects
            .filter(pk__in=participant_ids)
            .values_list("id", "username")
        )
    }

    results = (
        ContestResult.objects
        .filter(contest=contest, user_id__in=participant_ids)
        .select_related("ouverture")
    )

    results_by_user = defaultdict(list)
    for r in results:
        results_by_user[r.user_id].append(r)

    # DOIT RESTER UN DICT POUR LE TEMPLATE
    user_results_map = {
        r.ouverture_id: r
        for r in results
        if r.user_id == request.user.id
    }

    # =====================================================
    # COMPTAGES POUR SCORING
    # =====================================================
    if contest.is_permanent:
        counts_by_opening, openings_by_user = compute_permanent_success(
            contest=contest,
            inscrit_ids=participant_ids,
            ouverture_ids=ouverture_ids,
            relais_en_tete=relais_en_tete,
        )
    else:
        counts_by_opening = compute_non_permanent_counts(contest)
        openings_by_user = {}

    # =====================================================
    # DONE IDS (badge topo)
    # =====================================================
    if contest.is_permanent:
        done_ids = set(openings_by_user.get(request.user.id, {}).keys())
    else:
        done_ids = {
            r.ouverture_id
            for r in results_by_user.get(request.user.id, [])
            if r.has_top
        }

    # =====================================================
    # SCORE INDIVIDUEL
    # =====================================================
    def calc_score(user_id: int) -> dict:
        score = 0.0
        secondary = 0

        # -------- SCORE INITIAL (HÉRITAGE)
        inscription = inscription_by_user.get(user_id)
        if inscription:
            initialize_score_initial(inscription)
            score_initial = inscription.score_initial or 0
        else:
            score_initial = 0

        # -------- SCORE DU CONTEST COURANT
        if contest.is_permanent:
            user_openings = openings_by_user.get(user_id, {})
            if contest.format == Contest.CLASSIC:
                score = float(len(user_openings))
            else:
                for oid in user_openings:
                    total = counts_by_opening.get(oid, 0)
                    if total > 0:
                        score += 1000 / total
        else:
            for r in results_by_user.get(user_id, []):
                if r.has_top:
                    if contest.format == Contest.CLASSIC:
                        score += 1
                    else:
                        total = counts_by_opening.get(r.ouverture_id, 0)
                        if total > 0:
                            score += 1000 / total

            secondary = sum(
                (r.degaines_reached or 0) + (1 if r.has_zone else 0)
                for r in results_by_user.get(user_id, [])
            )

        # -------- SCORE FINAL
        score += score_initial

        return {
            "user_id": int(user_id),
            "username": usernames.get(int(user_id), "Utilisateur inconnu"),
            "score": int(score),
            "secondary_score": secondary,
            "genre": genre_map.get(int(user_id), ""),
        }

    all_scores = [calc_score(uid) for uid in participant_ids]

    # =====================================================
    # CLASSEMENTS INDIVIDUELS
    # =====================================================
    classement_general = sorted(
        all_scores,
        key=lambda x: (x["score"], x["secondary_score"]),
        reverse=True
    )
    for i, r in enumerate(
        assign_ranks_with_ties(classement_general, keys=("score", "secondary_score"))
    ):
        classement_general[i]["rank"] = r

    classement_femme = sorted(
        [dict(u) for u in all_scores if u["genre"] == "F"],
        key=lambda x: (x["score"], x["secondary_score"]),
        reverse=True
    )
    for i, r in enumerate(
        assign_ranks_with_ties(classement_femme, keys=("score", "secondary_score"))
    ):
        classement_femme[i]["rank"] = r

    classement_homme = sorted(
        [dict(u) for u in all_scores if u["genre"] == "M"],
        key=lambda x: (x["score"], x["secondary_score"]),
        reverse=True
    )
    for i, r in enumerate(
        assign_ranks_with_ties(classement_homme, keys=("score", "secondary_score"))
    ):
        classement_homme[i]["rank"] = r

    # =====================================================
    # CLASSEMENT PAR ÉQUIPE
    # =====================================================
    classement_teams = []

    if contest.is_team_contest:
        teams = Team.objects.filter(contest=contest).prefetch_related("members")

        classement_teams = compute_team_scores(
            contest=contest,
            teams=teams,
            results=results,
            counts_by_opening=counts_by_opening,
            current_user_id=request.user.id,
        )

        classement_teams = sorted(
            classement_teams,
            key=lambda x: x["score"],
            reverse=True
        )

        for i, r in enumerate(
            assign_ranks_with_ties(classement_teams, keys="score")
        ):
            classement_teams[i]["rank"] = r

    # =====================================================
    # TOPO
    # =====================================================
    topo = build_topo_info(
        contest=contest,
        ouvertures=ouvertures,
        nb_by_opening=counts_by_opening,
    )

    for row in topo:
        o = row["ouverture"]
        result = user_results_map.get(o.id)

        if contest.format != Contest.CLASSIC:
            if result and result.has_top:
                total = counts_by_opening.get(o.id, 0)
                if total > 0:
                    row["info"] = f"{int(1000 / total)} pts"

    # =====================================================
    # ONGLET ACTIF
    # =====================================================
    allowed_tabs = ["general", "femme", "homme"]
    if contest.is_team_contest:
        allowed_tabs.insert(0, "teams")

    active_classement = request.GET.get("classement")
    if active_classement not in allowed_tabs:
        active_classement = "teams" if contest.is_team_contest else "general"

    # =====================================================
    # RENDER
    # =====================================================
    return render(request, "contest/classement_topo/classement_topo.html", {
        "contest": contest,
        "classement_general": classement_general,
        "classement_femme": classement_femme,
        "classement_homme": classement_homme,
        "classement_teams": classement_teams,
        "topo": topo,
        "user_results_map": user_results_map,
        "relais_en_tete": relais_en_tete,
        "done_ids": list(done_ids),
        "active_classement": active_classement,
    })
