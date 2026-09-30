# applications/staff_admin/views/contest_ouverture_detail.py

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from applications.contest.models import Contest, Inscription, ContestResult
from applications.core.models import Seance
from applications.staff_admin.decorators import staff_required
from django.utils.timezone import now


# noinspection DuplicatedCode
@staff_required
def contest_ouverture_detail_view(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    ouvertures = contest.ouvertures.all().select_related("salle")

    # Participants "actifs" selon le type de contest
    if contest.is_payant:
        inscriptions_qs = Inscription.objects.filter(
            contest=contest, status=Inscription.Status.ACCEPTED
        )
    else:
        inscriptions_qs = Inscription.objects.filter(contest=contest).exclude(
            status=Inscription.Status.REFUSED
        )

    inscriptions = inscriptions_qs.values_list("user_id", flat=True)

    # 🔵 Gestion de la grimpe en tête
    relais_en_tete = contest.salle.relais_en_tete if contest.salle and contest.salle.relais_en_tete else []

    if contest.is_permanent:
        # 🔵 Contest permanent : Seance
        reussites = []

        for ouverture in ouvertures:
            base_qs = Seance.objects.filter(
                ouverture=ouverture,
                user_id__in=inscriptions,
                created_at__lte=contest.end_date if contest.end_date else now()
            )

            if not ouverture.bloc and ouverture.relais in relais_en_tete:
                # 🔵 Voie grimpable en tête → uniquement nb_top_lead
                nb_reussites = (
                    base_qs.filter(nb_top_lead__gt=0)
                    .values("user").distinct().count()
                )
            else:
                # 🟠 Sinon (moulinette ou bloc) → nb_top ou nb_top_lead
                nb_reussites = (
                    base_qs.filter(Q(nb_top__gt=0) | Q(nb_top_lead__gt=0))
                    .values("user").distinct().count()
                )

            reussites.append({
                "ouverture": ouverture.id,
                "nb_reussites": nb_reussites,
            })

    else:
        # 🟠 Contest événementiel : ContestResult
        reussites = (
            ContestResult.objects
            .filter(
                contest=contest,
                ouverture__in=ouvertures,
                user_id__in=inscriptions,
                has_top=True
            )
            .values("ouverture")
            .annotate(nb_reussites=Count("user", distinct=True))
        )

    # Mapping ouverture_id → nb_reussites
    nb_reussites_map = {entry["ouverture"]: entry["nb_reussites"] for entry in reussites}

    data = []
    for o in ouvertures:
        nb_reussites = nb_reussites_map.get(o.id, 0)
        points_prochain = int(1000 / (nb_reussites + 1)) if contest.format == Contest.POINTS_1000 else None

        data.append({
            "ouverture": o,
            "nb_reussites": nb_reussites,
            "points_prochain": points_prochain,
        })

    return render(request, "staff_admin/contest_ouverture_detail/contest_ouverture_detail.html", {
        "contest": contest,
        "ouvertures_data": data,
    })
