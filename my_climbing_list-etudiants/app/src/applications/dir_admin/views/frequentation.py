# applications/dir_admin/views/frequentation.py

from django.shortcuts import render
from applications.dir_admin.decorators.superuser_required import superuser_required
from django.utils.safestring import mark_safe
from applications.dir_admin.utils.retention import get_retention_stats
import os

# === Constantes === #
CACHE_DIR = "cache/dir_admin/"
FREQUENTATION_CACHE_FILE = os.path.join(CACHE_DIR, "frequentation.html")
RETENTION_CACHE_FILE = os.path.join(CACHE_DIR, "retention.html")


@superuser_required
def frequentation_view(request):
    """
    Vue de fréquentation pour la direction (superuser uniquement).
    """

    graph_html = ""
    graph_salle_html = ""
    retention_graph_html = ""

    # === Lecture du cache fréquentation === #
    if os.path.exists(FREQUENTATION_CACHE_FILE):
        with open(FREQUENTATION_CACHE_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
            if "<hr>" in html_content:
                graph_html, graph_salle_html = html_content.split("<hr>", 1)
            else:
                graph_html = html_content

    # === Lecture du cache rétention (graphique) === #
    if os.path.exists(RETENTION_CACHE_FILE):
        with open(RETENTION_CACHE_FILE, "r", encoding="utf-8") as f:
            retention_graph_html = f.read()

    # === Calcul dynamique des stats === #
    retention_stats = get_retention_stats()

    # === Contexte === #
    context = {
        "graph_html": mark_safe(
            graph_html or "<p>Données de fréquentation non disponibles.</p>"
        ),
        "graph_salle_html": mark_safe(graph_salle_html),
        "retention_graph_html": mark_safe(retention_graph_html),
        "retention_stats": retention_stats,
    }

    return render(
        request,
        "dir_admin/frequentation/frequentation.html",
        context,
    )
