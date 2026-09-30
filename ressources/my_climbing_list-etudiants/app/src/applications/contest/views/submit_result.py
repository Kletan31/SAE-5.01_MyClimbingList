# applications/contest/views/submit_result.py

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from applications.contest.models import Contest, ContestResult
from applications.core.models import Ouverture


@login_required
def submit_contest_results_view(request, contest_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    contest = get_object_or_404(Contest, pk=contest_id)

    try:
        data = json.loads(request.body)
        changes = data.get("changes", [])
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "Données invalides"}, status=400)

    for change in changes:
        ouverture_id = change.get("ouverture_id")
        result_type = change.get("type")
        value = int(change.get("value", 0))

        if not ouverture_id or not result_type:
            continue  # Ignore les entrées mal formées

        ouverture = get_object_or_404(Ouverture, pk=ouverture_id)

        result, created = ContestResult.objects.get_or_create(
            contest=contest,
            user=request.user,
            ouverture=ouverture,
        )

        if result_type == "top":
            result.has_top = bool(value)
        elif result_type == "zone":
            result.has_zone = bool(value)
        elif result_type == "degaine":
            result.degaines_reached = value
        else:
            continue  # Ignore les types inconnus

        # Si tout est vide, on supprime l'entrée
        if not (result.has_top or result.has_zone or result.degaines_reached):
            result.delete()
        else:
            result.save()

    return JsonResponse({"success": True})
