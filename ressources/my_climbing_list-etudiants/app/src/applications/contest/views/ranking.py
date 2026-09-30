# applications/contest/views/ranking.py

from pathlib import Path
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.timezone import localdate

from bs4 import BeautifulSoup

CACHE_DIR = Path("cache/public_contests")


@login_required
def ranking_view(request):
    """
    Classement Elo global (Top 100) intégré dans l'app mobile.
    - Source : HTML statique pré-généré
    - Injection UNIQUEMENT de la vue mobile (id="mobileView")
    - Mise en évidence de l'utilisateur connecté si présent
    """

    user = request.user
    bloc = request.GET.get("bloc") == "1"

    filename = (
        "climber_ranking_bloc.html"
        if bloc else
        "climber_ranking_voie.html"
    )

    html_path = CACHE_DIR / filename

    ranking_html = "<p class='text-center'>Classement indisponible</p>"
    user_rank = None

    if html_path.exists():
        full_html = html_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(full_html, "html.parser")

        # Extraction de la vue mobile
        mobile_view = soup.find(id="mobileView")

        if mobile_view:
            # Recherche de la card utilisateur
            user_card = mobile_view.find(
                "div",
                class_="climber-card",
                attrs={"data-user-id": str(user.id)}
            )

            if user_card:
                # Ajout de la classe active
                existing_classes = user_card.get("class", [])
                if "active" not in existing_classes:
                    user_card["class"] = existing_classes + ["active"]

                # Récupération optionnelle du rang
                user_rank = user_card.get("data-rank")

            ranking_html = str(mobile_view)

    context = {
        "ranking_html": mark_safe(ranking_html),
        "bloc": bloc,
        "user_id": user.id,
        "user_rank": user_rank,  # utile plus tard
        "date": localdate() - timedelta(days=1),
    }

    return render(
        request,
        "contest/ranking/ranking.html",
        context,
    )
