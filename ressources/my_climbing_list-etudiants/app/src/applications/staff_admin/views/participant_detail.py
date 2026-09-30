# applications/staff_admin/views/participant_detail.py

from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now
from applications.contest.models import Contest, Inscription, ContestResult
from applications.core.models import Seance
from django.contrib.auth.models import User
from applications.staff_admin.decorators import staff_required


# noinspection DuplicatedCode
@staff_required
def participant_detail_view(request, contest_id, user_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    participant = get_object_or_404(User, pk=user_id)

    # Participants "actifs" selon le type de contest
    if contest.is_payant:
        inscrits_ids = (Inscription.objects
                        .filter(contest=contest, status=Inscription.Status.ACCEPTED)
                        .values_list("user", flat=True))
    else:
        inscrits_ids = (Inscription.objects
                        .filter(contest=contest)
                        .exclude(status=Inscription.Status.REFUSED)
                        .values_list("user", flat=True))

    resultats = []
    grimpeurs_par_ouverture = {}
    total_score = 0

    if contest.is_permanent:
        ouvertures = contest.ouvertures.all().select_related("salle")
        salle = contest.salle
        relais_en_tete = salle.relais_en_tete if salle and salle.relais_en_tete else []

        seances = (Seance.objects
                   .filter(
                       user=participant,
                       ouverture__in=ouvertures,
                       created_at__lte=contest.end_date if contest.end_date else now()
                   )
                   .select_related("ouverture")
                   .distinct())

        if contest.format != Contest.CLASSIC:
            for o in ouvertures:
                base_qs = (Seance.objects
                           .filter(
                               ouverture=o,
                               user_id__in=inscrits_ids,
                               created_at__lte=contest.end_date if contest.end_date else now()
                           ))

                if not o.bloc and o.relais in relais_en_tete:
                    nb = (base_qs.filter(nb_top_lead__gt=0).values("user").distinct().count())
                else:
                    nb = (base_qs.filter(Q(nb_top__gt=0) | Q(nb_top_lead__gt=0)).values("user").distinct().count())

                grimpeurs_par_ouverture[o.id] = nb

        for s in seances:
            o = s.ouverture
            if not o:
                continue

            if not o.bloc and o.relais in relais_en_tete:
                successful = bool(s.nb_top_lead and s.nb_top_lead > 0)
            else:
                successful = bool((s.nb_top and s.nb_top > 0) or (s.nb_top_lead and s.nb_top_lead > 0))

            if not successful:
                continue

            if contest.format == Contest.CLASSIC:
                points = 1
            else:
                total_grimpeurs = grimpeurs_par_ouverture.get(o.id, 0)
                points = (1000 / total_grimpeurs) if total_grimpeurs > 0 else 0

            resultats.append({
                "ouverture": o,
                "points": int(points),
                "has_top": True,
                "has_zone": None,
                "degaines_reached": None,
            })
            total_score += points

        resultats.sort(key=lambda x: (
            0 if not x["has_top"] else 1,  # D'abord tops
            x["ouverture"].niveau or ""     # Ensuite cotation décroissante
        ), reverse=True)

    else:
        results = (ContestResult.objects
                   .filter(contest=contest, user=participant)
                   .select_related("ouverture"))

        if contest.format != Contest.CLASSIC:
            grimpeurs_par_ouverture = (ContestResult.objects
                                       .filter(contest=contest, has_top=True)
                                       .values("ouverture")
                                       .annotate(total=Count("user", distinct=True)))
            grimpeurs_par_ouverture = {item["ouverture"]: item["total"] for item in grimpeurs_par_ouverture}

        for r in results:
            if not (r.has_top or r.has_zone or r.degaines_reached):
                continue

            if contest.format == Contest.CLASSIC:
                points = 1 if r.has_top else 0
            else:
                total_grimpeurs = grimpeurs_par_ouverture.get(r.ouverture.id, 0)
                points = (1000 / total_grimpeurs) if (r.has_top and total_grimpeurs > 0) else 0

            resultats.append({
                "ouverture": r.ouverture,
                "points": int(points),
                "has_top": r.has_top,
                "has_zone": r.has_zone,
                "degaines_reached": r.degaines_reached,
            })
            total_score += points

        resultats.sort(key=lambda x: (
            0 if not x["has_top"] else 1,      # D'abord tops
            0 if x["ouverture"].bloc else 1,   # Ensuite voies avant blocs
            x["ouverture"].niveau or ""        # Enfin cotation décroissante
        ), reverse=True)

    return render(request, "staff_admin/participant_detail/participant_detail.html", {
        "participant": participant,
        "contest": contest,
        "resultats": resultats,
        "total_score": int(total_score),
    })
