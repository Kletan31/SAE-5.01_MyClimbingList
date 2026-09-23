# applications/staff_admin/views/frequentation.py

from applications.staff_admin.decorators import staff_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import os

CACHE_DIR = "cache/dir_admin/"


def _load_graph_html(file_path, empty_message):
    """
    Charge un fichier HTML de graphe s'il existe,
    sinon retourne un message par défaut.
    """
    if not os.path.exists(file_path):
        return f"<p>{empty_message}</p>"

    with open(file_path, "r") as f:
        return mark_safe(f.read())


@staff_required
def salle_frequentation_view(request):
    user = request.user
    salle = user.profile.salle_voie

    # Sécurité minimale
    if salle is None:
        return render(request, "staff_admin/frequentation/frequentation.html", {
            "salle": None,
            "graph_salle_html": "<p>Aucune salle associée.</p>",
            "graph_global_html": "",
        })

    salle_id = salle.id

    # ----------------------------
    # Graph fréquentation SALLE
    # ----------------------------
    salle_graph_path = os.path.join(
        CACHE_DIR,
        "frequentation_salles",
        f"{salle_id}.html",
    )

    graph_salle_html = _load_graph_html(
        salle_graph_path,
        "Aucune donnée disponible pour cette salle."
    )

    # ----------------------------
    # Graph fréquentation GLOBAL
    # ----------------------------
    global_graph_path = os.path.join(
        CACHE_DIR,
        "frequentation.html",
    )

    graph_global_html = _load_graph_html(
        global_graph_path,
        "Aucune donnée globale disponible."
    )

    return render(
        request,
        "staff_admin/frequentation/frequentation.html",
        {
            "salle": salle,
            "graph_salle_html": graph_salle_html,
            "graph_global_html": graph_global_html,
        }
    )
