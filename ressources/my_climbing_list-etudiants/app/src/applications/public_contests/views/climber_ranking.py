# applications/public_contests/views/climber_ranking.py

from pathlib import Path

from django.http import HttpResponse


CACHE_DIR = Path("cache/public_contests")


def climber_ranking_view(request):
    """
    Classement Elo public journalier (HTML pré-généré).
    """

    bloc = request.GET.get("bloc") == "1"

    filename = (
        "climber_ranking_bloc.html"
        if bloc else
        "climber_ranking_voie.html"
    )

    html_path = CACHE_DIR / filename

    if not html_path.exists():
        # Fallback propre si la commande n'a pas encore tourné
        return HttpResponse(
            "Classement indisponible pour le moment.",
            status=503,
            content_type="text/plain",
        )

    return HttpResponse(
        html_path.read_text(encoding="utf-8"),
        content_type="text/html",
    )
