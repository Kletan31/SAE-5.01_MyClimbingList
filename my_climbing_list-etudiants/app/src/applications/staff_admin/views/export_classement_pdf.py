# applications/staff_admin/views/export_classement_pdf.py

from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

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
def export_classement_pdf_view(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)

    # =====================================================
    # INSCRIPTIONS ACTIVES
    # =====================================================
    inscriptions = Inscription.objects.filter(contest=contest)

    if contest.is_payant:
        inscriptions = inscriptions.filter(status=Inscription.Status.ACCEPTED)
    else:
        inscriptions = inscriptions.exclude(status=Inscription.Status.REFUSED)

    # Initialisation score_initial (idempotent)
    for ins in inscriptions.select_related("user"):
        initialize_score_initial(ins)

    inscrit_ids = list(inscriptions.values_list("user_id", flat=True))
    profils = Profile.objects.filter(user_id__in=inscrit_ids)
    genre_map = {p.user_id: p.gender for p in profils}

    # =====================================================
    # PDF SETUP
    # =====================================================
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    page_number = 1

    # -------------------------
    # Outils PDF
    # -------------------------
    def footer():
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawCentredString(width / 2, 1.5 * cm, f"Page {page_number}")

    def new_page():
        nonlocal page_number
        footer()
        pdf.showPage()
        page_number += 1

    def draw_title(title):
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(width / 2, height - 2 * cm, f"{title} – {contest.name}")
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawCentredString(
            width / 2, height - 2.8 * cm, now().strftime("%d/%m/%Y")
        )

    def draw_individual_classement(title, rows, ranks):
        y = height - 4 * cm
        draw_title(title)

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, y, "Rang")
        pdf.drawString(4 * cm, y, "Nom")
        pdf.drawString(10 * cm, y, "Prénom")
        pdf.drawString(16 * cm, y, "Score")
        y -= 0.8 * cm

        pdf.setFont("Helvetica", 11)
        for i, r in enumerate(rows):
            if y < 2 * cm:
                new_page()
                y = height - 4 * cm

            pdf.drawString(2 * cm, y, str(ranks[i]))
            pdf.drawString(4 * cm, y, r["nom"])
            pdf.drawString(10 * cm, y, r["prenom"])
            pdf.drawString(16 * cm, y, str(r["score"]))
            y -= 0.6 * cm

        new_page()

    # =====================================================
    # CLASSEMENT PAR ÉQUIPE (si applicable)
    # =====================================================
    if contest.is_team_contest:
        teams = contest.teams.prefetch_related("members")
        results = contest.results.select_related("ouverture")

        classement_teams = compute_team_scores(
            contest=contest,
            teams=teams,
            results=results,
            counts_by_opening={},
            current_user_id=None,
        )

        classement_teams.sort(key=lambda x: x["score"], reverse=True)
        ranks_teams = assign_ranks_with_ties(classement_teams)

        y = height - 4 * cm
        draw_title("Classement par équipe")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, y, "Rang")
        pdf.drawString(5 * cm, y, "Équipe")
        pdf.drawString(15 * cm, y, "Score")
        y -= 0.8 * cm

        pdf.setFont("Helvetica", 11)
        for i, row in enumerate(classement_teams):
            if y < 2 * cm:
                new_page()
                y = height - 4 * cm

            pdf.drawString(2 * cm, y, str(ranks_teams[i]))
            pdf.drawString(5 * cm, y, row["team_name"])
            pdf.drawString(15 * cm, y, str(row["score"]))
            y -= 0.6 * cm

        new_page()

    # =====================================================
    # CLASSEMENTS INDIVIDUELS (TOUJOURS)
    # =====================================================
    rows = []
    for ins in inscriptions.select_related("user"):
        base = ins.score_initial or 0
        intrinsic = compute_user_score(
            contest=contest,
            user_id=ins.user_id,
        )
        total = base + intrinsic

        rows.append({
            "user_id": ins.user_id,
            "nom": (ins.user.last_name or ins.user.username).upper(),
            "prenom": ins.user.first_name or "",
            "score": total,
        })

    # --------- Général ----------
    rows.sort(key=lambda x: x["score"], reverse=True)
    ranks_general = assign_ranks_with_ties(rows)
    draw_individual_classement("Classement général", rows, ranks_general)

    # --------- Par genre ----------
    femmes = [r for r in rows if genre_map.get(r["user_id"]) == "F"]
    hommes = [r for r in rows if genre_map.get(r["user_id"]) == "M"]

    femmes.sort(key=lambda x: x["score"], reverse=True)
    hommes.sort(key=lambda x: x["score"], reverse=True)

    ranks_f = assign_ranks_with_ties(femmes)
    ranks_h = assign_ranks_with_ties(hommes)

    draw_individual_classement("Classement femmes", femmes, ranks_f)
    draw_individual_classement("Classement hommes", hommes, ranks_h)

    # =====================================================
    # FINALISATION
    # =====================================================
    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="classement_{contest.id}.pdf"'
    )
    return response
