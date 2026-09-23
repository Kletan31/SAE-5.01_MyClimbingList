# applications/staff_admin/views/export_classement_csv.py
import csv

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from applications.staff_admin.decorators import staff_required
from applications.contest.models import Contest, Inscription
from applications.custom_auth.models import Profile

from applications.contest.utils.scoring import (
    compute_user_score,
    compute_team_scores,
    assign_ranks_with_ties,
)
from applications.contest.utils.score_initialization import initialize_score_initial


@staff_required
def export_classement_csv_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    # =====================================================
    # INSCRIPTIONS ACTIVES
    # =====================================================
    inscriptions = Inscription.objects.filter(contest=contest)
    if contest.is_payant:
        inscriptions = inscriptions.filter(status=Inscription.Status.ACCEPTED)
    else:
        inscriptions = inscriptions.exclude(status=Inscription.Status.REFUSED)

    # Initialisation du score initial (idempotent)
    for ins in inscriptions.select_related("user"):
        initialize_score_initial(ins)

    inscrit_ids = list(inscriptions.values_list("user_id", flat=True))

    profils = Profile.objects.filter(user_id__in=inscrit_ids)
    genre_map = {p.user_id: p.gender for p in profils}

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="classement_{contest.id}.csv"'
    )
    writer = csv.writer(response)

    # =====================================================
    # CONTEST PAR ÉQUIPE
    # =====================================================
    if contest.is_team_contest:
        teams = contest.teams.prefetch_related("members")
        results = contest.results.select_related("ouverture")

        classement = compute_team_scores(
            contest=contest,
            teams=teams,
            results=results,
            counts_by_opening={},
            current_user_id=None,
        )

        classement.sort(key=lambda x: x["score"], reverse=True)
        ranks = assign_ranks_with_ties(classement)

        writer.writerow(["Classement par équipe"])
        writer.writerow(["Rang", "Équipe", "Score"])

        for i, row in enumerate(classement):
            writer.writerow([
                ranks[i],
                row["team_name"],
                row["score"],
            ])

        return response

    # =====================================================
    # CONTEST INDIVIDUEL
    # =====================================================
    rows = []
    for ins in inscriptions.select_related("user"):
        score_intrinsic = compute_user_score(
            contest=contest,
            user_id=ins.user_id,
        )
        total_score = (ins.score_initial or 0) + score_intrinsic

        rows.append({
            "user_id": ins.user_id,
            "nom": (ins.user.last_name or ins.user.username).upper(),
            "prenom": ins.user.first_name or "",
            "score": total_score,
        })

    # ---------------------
    # Classement général
    # ---------------------
    rows.sort(key=lambda x: x["score"], reverse=True)
    ranks_general = assign_ranks_with_ties(rows)

    def write_section(title, data, ranks):
        writer.writerow([])
        writer.writerow([title])
        writer.writerow(["Rang", "Nom", "Prénom", "Score"])
        for i, row in enumerate(data):
            writer.writerow([
                ranks[i],
                row["nom"],
                row["prenom"],
                row["score"],
            ])

    write_section("Classement Général", rows, ranks_general)

    # ---------------------
    # Classements par genre
    # ---------------------
    femmes = [r for r in rows if genre_map.get(r["user_id"]) == "F"]
    hommes = [r for r in rows if genre_map.get(r["user_id"]) == "M"]

    femmes.sort(key=lambda x: x["score"], reverse=True)
    hommes.sort(key=lambda x: x["score"], reverse=True)

    ranks_f = assign_ranks_with_ties(femmes)
    ranks_h = assign_ranks_with_ties(hommes)

    write_section("Classement Femmes", femmes, ranks_f)
    write_section("Classement Hommes", hommes, ranks_h)

    return response
