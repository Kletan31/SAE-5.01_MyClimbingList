import csv
from io import BytesIO, StringIO

from django.http import HttpResponse
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from applications.route_event.models import RouteEventPhase
from applications.route_event.services.ranking import get_route_event_ranking


GENDER_SECTIONS = [
    (None, "Général"),
    ("M", "Masculin"),
    ("F", "Féminin"),
]


def get_ranking_export_sections(event):
    sections = []

    phase_options = [
        (None, "Global"),
    ]

    phases = (
        RouteEventPhase.objects
        .filter(event=event)
        .order_by("start_time")
    )

    for phase in phases:
        phase_options.append(
            (phase, phase.name)
        )

    for phase, phase_label in phase_options:
        for gender, gender_label in GENDER_SECTIONS:
            ranking_rows = get_route_event_ranking(
                event=event,
                phase=phase,
                gender=gender,
            )

            sections.append(
                {
                    "title": f"{phase_label} - {gender_label}",
                    "phase": phase,
                    "gender": gender,
                    "ranking_rows": ranking_rows,
                }
            )

    return sections


def build_ranking_csv_response(event):
    response = HttpResponse(
        content_type="text/csv; charset=utf-8",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="classements_{event.slug}.csv"'
    )

    response.write("\ufeff")

    writer = csv.writer(
        response,
        delimiter=";",
    )

    writer.writerow(
        [
            event.name,
        ]
    )

    writer.writerow(
        [
            "Export généré le",
            timezone.localtime().strftime("%d/%m/%Y %H:%M"),
        ]
    )

    writer.writerow([])

    sections = get_ranking_export_sections(event)

    for section in sections:
        writer.writerow(
            [
                section["title"],
            ]
        )

        writer.writerow(
            [
                "Rang",
                "Prénom",
                "Nom",
                "Genre",
                "Créneau",
                "Points qualification",
                "Voies saisies",
            ]
        )

        for row in section["ranking_rows"]:
            participant = row["participant"]

            writer.writerow(
                [
                    row["rank"],
                    participant.first_name,
                    participant.last_name,
                    participant.get_gender_display(),
                    participant.phase.name,
                    row["qualification_points"],
                    row["routes_done"],
                ]
            )

        writer.writerow([])

    return response


def build_ranking_pdf_response(event):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            f"Classements - {event.name}",
            styles["Title"],
        )
    )

    elements.append(
        Paragraph(
            f"Export généré le {timezone.localtime().strftime('%d/%m/%Y à %H:%M')}",
            styles["Normal"],
        )
    )

    elements.append(
        Spacer(1, 0.5 * cm)
    )

    sections = get_ranking_export_sections(event)

    for section_index, section in enumerate(sections):
        if section_index > 0:
            elements.append(
                PageBreak()
            )

        elements.append(
            Paragraph(
                section["title"],
                styles["Heading2"],
            )
        )

        elements.append(
            Spacer(1, 0.3 * cm)
        )

        table_data = [
            [
                "Rang",
                "Prénom",
                "Nom",
                "Genre",
                "Créneau",
                "Points",
                "Voies",
            ]
        ]

        for row in section["ranking_rows"]:
            participant = row["participant"]

            table_data.append(
                [
                    row["rank"],
                    participant.first_name,
                    participant.last_name,
                    participant.get_gender_display(),
                    participant.phase.name,
                    row["qualification_points"],
                    row["routes_done"],
                ]
            )

        if len(table_data) == 1:
            table_data.append(
                [
                    "-",
                    "Aucun participant",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )

        table = Table(
            table_data,
            repeatRows=1,
            colWidths=[
                1.3 * cm,
                4 * cm,
                4 * cm,
                3 * cm,
                4 * cm,
                3 * cm,
                2 * cm,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172039")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (1, 1), (2, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4EFE5")]),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        elements.append(table)

    document.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(
        pdf,
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="classements_{event.slug}.pdf"'
    )

    return response