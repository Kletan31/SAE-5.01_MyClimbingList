# applications/public_contests/views/contest_detail.py

from datetime import timedelta
from collections import defaultdict

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from applications.contest.models import Contest, Inscription, ContestResult, Team
from applications.custom_auth.models import Profile
from applications.contest.utils.scoring import (
    compute_non_permanent_counts,
    assign_ranks_with_ties,
    compute_team_scores,
)

User = get_user_model()


def contest_detail_view(request, contest_id):
    now_ = now()
    grace_period = timedelta(days=1)

    # =====================================================
    # CONTEST PUBLIC (non permanent)
    # =====================================================
    contest = get_object_or_404(
        Contest,
        pk=contest_id,
        is_active=True,
        is_permanent=False,
        start_date__lte=now_,
    )

    # =====================================================
    # VISIBILITÉ (fin + 1 jour)
    # =====================================================
    if contest.end_date:
        is_visible = contest.end_date + grace_period >= now_
        is_running = contest.start_date <= now_ <= contest.end_date
    else:
        is_visible = True
        is_running = True

    if not is_visible:
        raise Http404()

    # =====================================================
    # PARTICIPANTS (SOURCE DE VÉRITÉ)
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
    # DONNÉES UTILISATEURS (⚠️ CORRIGÉ ICI)
    # =====================================================
    profils = Profile.objects.filter(user_id__in=participant_ids)
    genre_map = {p.user_id: p.gender for p in profils}

    usernames = {
        u.id: u.username
        for u in User.objects.filter(id__in=participant_ids)
    }

    # =====================================================
    # RÉSULTATS (PEUVENT ÊTRE VIDES)
    # =====================================================
    results = (
        ContestResult.objects
        .filter(contest=contest, user_id__in=participant_ids)
        .select_related("ouverture")
    )

    results_by_user = defaultdict(list)
    for r in results:
        results_by_user[r.user_id].append(r)

    # =====================================================
    # COMPTAGES POUR SCORING
    # =====================================================
    counts_by_opening = compute_non_permanent_counts(contest)

    # =====================================================
    # SCORE INDIVIDUEL
    # =====================================================
    def calc_score(user_id: int) -> dict:
        score = 0.0
        secondary = 0

        for r in results_by_user.get(user_id, []):
            if r.has_top:
                if contest.format == Contest.CLASSIC:
                    score += 1
                else:
                    total = counts_by_opening.get(r.ouverture_id, 0)
                    if total > 0:
                        score += 1000 / total

            secondary += (r.degaines_reached or 0) + (1 if r.has_zone else 0)

        return {
            "user_id": user_id,
            "username": usernames.get(user_id, "Utilisateur"),
            "score": int(score),
            "secondary_score": secondary,
            "genre": genre_map.get(user_id),
        }

    all_scores = [calc_score(uid) for uid in participant_ids]

    # =====================================================
    # CLASSEMENTS INDIVIDUELS
    # =====================================================
    classement_general = sorted(
        all_scores,
        key=lambda x: (x["score"], x["secondary_score"]),
        reverse=True,
    )
    for i, r in enumerate(assign_ranks_with_ties(classement_general)):
        classement_general[i]["rank"] = r

    classement_femme = [dict(u) for u in classement_general if u["genre"] == "F"]
    for i, r in enumerate(assign_ranks_with_ties(classement_femme)):
        classement_femme[i]["rank"] = r

    classement_homme = [dict(u) for u in classement_general if u["genre"] == "M"]
    for i, r in enumerate(assign_ranks_with_ties(classement_homme)):
        classement_homme[i]["rank"] = r

    # =====================================================
    # CLASSEMENT PAR ÉQUIPE (PUBLIC)
    # =====================================================
    classement_teams = []

    if contest.is_team_contest:
        teams = Team.objects.filter(contest=contest).prefetch_related("members")

        classement_teams = compute_team_scores(
            contest=contest,
            teams=teams,
            results=results,
            counts_by_opening=counts_by_opening,
            current_user_id=-1,  # public → aucun utilisateur mis en avant
        )

        classement_teams = sorted(
            classement_teams,
            key=lambda x: x["score"],
            reverse=True,
        )

        for i, r in enumerate(assign_ranks_with_ties(classement_teams)):
            classement_teams[i]["rank"] = r

    # =====================================================
    # RENDER
    # =====================================================
    return render(
        request,
        "public_contests/contest_detail/contest_detail.html",
        {
            "contest": contest,
            "is_running": is_running,
            "classement_general": classement_general,
            "classement_femme": classement_femme,
            "classement_homme": classement_homme,
            "classement_teams": classement_teams,
        }
    )
