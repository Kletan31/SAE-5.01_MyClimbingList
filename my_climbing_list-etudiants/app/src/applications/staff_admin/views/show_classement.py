# applications/staff_admin/views/show_classement.py

from django.shortcuts import get_object_or_404, render

from applications.staff_admin.decorators import staff_required
from applications.contest.models import Contest, Inscription, ContestResult, Team
from applications.custom_auth.models import Profile

from applications.contest.utils.scoring import (
    compute_user_score,
    compute_team_scores,
    compute_permanent_success,
    compute_non_permanent_counts,
    assign_ranks_with_ties,
)


@staff_required
def show_classement_view(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)

    # =====================================================
    # INSCRIPTIONS ACTIVES
    # =====================================================
    inscriptions = Inscription.objects.filter(contest=contest)
    if contest.is_payant:
        inscriptions = inscriptions.filter(status=Inscription.Status.ACCEPTED)
    else:
        inscriptions = inscriptions.exclude(status=Inscription.Status.REFUSED)

    inscrit_ids = list(inscriptions.values_list("user_id", flat=True))

    # =====================================================
    # BRANCHE ÉQUIPE
    # =====================================================
    if contest.is_team_contest:
        teams = (
            Team.objects
            .filter(contest=contest)
            .prefetch_related("members")
        )

        results = ContestResult.objects.filter(contest=contest)

        # Comptages par ouverture (cohérents avec le public)
        if contest.is_permanent:
            salle = contest.salle
            relais_en_tete = salle.relais_en_tete if salle and salle.relais_en_tete else []

            ouverture_ids = list(
                contest.ouvertures.values_list("id", flat=True)
            )

            counts_by_opening, _ = compute_permanent_success(
                contest=contest,
                inscrit_ids=inscrit_ids,
                ouverture_ids=ouverture_ids,
                relais_en_tete=relais_en_tete,
            )
        else:
            counts_by_opening = compute_non_permanent_counts(contest)

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
            reverse=True,
        )

        for i, r in enumerate(assign_ranks_with_ties(classement_teams)):
            classement_teams[i]["rank"] = r

        return render(
            request,
            "staff_admin/show_classement/show_classement.html",
            {
                "contest": contest,
                "is_team": True,
                "classement_equipe": classement_teams,
            },
        )

    # =====================================================
    # BRANCHE INDIVIDUELLE
    # =====================================================
    profils = Profile.objects.filter(user_id__in=inscrit_ids)
    genre_map = {p.user_id: p.gender for p in profils}

    # Scores intrinsèques (SANS score_initial)
    user_scores = {
        uid: compute_user_score(
            contest=contest,
            user_id=uid,
        )
        for uid in inscrit_ids
    }

    # Infos utilisateurs
    rows = inscriptions.values_list(
        "user_id",
        "user__first_name",
        "user__last_name",
        "user__username",
    )

    users_info = {
        uid: (fn, ln, un)
        for uid, fn, ln, un in rows
    }

    def build_classement(user_ids):
        classement = []
        for uid in user_ids:
            first_name, last_name, username = users_info.get(
                uid, ("", "", f"USER-{uid}")
            )
            classement.append({
                "user_id": uid,
                "nom": (last_name or username).upper(),
                "prenom": first_name or "",
                "score": user_scores.get(uid, 0),
            })
        classement.sort(key=lambda x: x["score"], reverse=True)
        return classement

    all_ids = inscrit_ids
    men_ids = [uid for uid in inscrit_ids if genre_map.get(uid) == "M"]
    women_ids = [uid for uid in inscrit_ids if genre_map.get(uid) == "F"]

    classement_general = build_classement(all_ids)
    classement_homme = build_classement(men_ids)
    classement_femme = build_classement(women_ids)

    # =====================================================
    # RANGS
    # =====================================================
    for i, r in enumerate(assign_ranks_with_ties(classement_general)):
        classement_general[i]["rank"] = r
        classement_general[i]["rank_general"] = r

    for i, r in enumerate(assign_ranks_with_ties(classement_homme)):
        classement_homme[i]["rank"] = r
        classement_homme[i]["rank_genre"] = r

    for i, r in enumerate(assign_ranks_with_ties(classement_femme)):
        classement_femme[i]["rank"] = r
        classement_femme[i]["rank_genre"] = r

    genre_ranks = {
        **{p["user_id"]: p["rank_genre"] for p in classement_homme},
        **{p["user_id"]: p["rank_genre"] for p in classement_femme},
    }

    for row in classement_general:
        row["rank_genre"] = genre_ranks.get(row["user_id"])

    return render(
        request,
        "staff_admin/show_classement/show_classement.html",
        {
            "contest": contest,
            "is_team": False,
            "classement_general": classement_general,
            "classement_homme": classement_homme,
            "classement_femme": classement_femme,
        },
    )
