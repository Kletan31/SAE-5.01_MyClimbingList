# applications/staff_admin/views/manage_team.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from applications.contest.models import Contest, Inscription, Team
from applications.staff_admin.decorators import staff_required

User = get_user_model()


def _parse_member_ids(raw: str) -> set[int]:
    """Transforme '1,2,3' -> {1,2,3}, ignore vides/espaces, évite ValueError."""
    ids = set()
    if not raw:
        return ids
    for tok in raw.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            ids.add(int(tok))
        except ValueError:
            # on ignore silencieusement les tokens invalides
            pass
    return ids


@staff_required
def manage_teams_view(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)

    if not contest.is_team_contest:
        return redirect("staff_admin:dashboard")

    # Participants "éligibles" selon le type de contest
    if contest.is_payant:
        inscriptions_qs = Inscription.objects.filter(
            contest=contest, status=Inscription.Status.ACCEPTED
        )
    else:
        inscriptions_qs = Inscription.objects.filter(contest=contest).exclude(
            status=Inscription.Status.REFUSED
        )

    eligible_user_ids = set(inscriptions_qs.values_list("user_id", flat=True))
    users_qs = User.objects.filter(id__in=eligible_user_ids).order_by("username")

    if request.method == "POST":
        if "create_team" in request.POST:
            name = request.POST.get("team_name", "").strip()
            member_ids = _parse_member_ids(request.POST.get("team_members", ""))

            # Restreindre aux éligibles
            member_ids &= eligible_user_ids

            if not name:
                messages.error(request, "Le nom de l’équipe est requis.")
                return redirect("staff_admin:manage_teams", contest_id=contest_id)

            # Empêcher qu'un membre soit dans deux équipes
            used_user_ids = set(
                Team.objects.filter(contest=contest)
                .values_list("members__id", flat=True)
            )
            valid_ids = member_ids - used_user_ids

            team = Team.objects.create(contest=contest, name=name)
            team.members.set(users_qs.filter(id__in=valid_ids))
            messages.success(request, f"Équipe « {team.name} » créée ({len(valid_ids)} membre(s)).")

        elif "update_team" in request.POST:
            team_id = request.POST.get("team_id")
            team = get_object_or_404(Team, id=team_id, contest=contest)
            name = request.POST.get("team_name", "").strip()
            member_ids = _parse_member_ids(request.POST.get("team_members", ""))

            # Restreindre aux éligibles
            member_ids &= eligible_user_ids

            other_teams_user_ids = set(
                Team.objects.filter(contest=contest).exclude(id=team.id)
                .values_list("members__id", flat=True)
            )
            valid_ids = member_ids - other_teams_user_ids

            if name:
                team.name = name
            team.members.set(users_qs.filter(id__in=valid_ids))
            team.save()
            messages.success(request, f"Équipe « {team.name} » mise à jour ({len(valid_ids)} membre(s)).")

        elif "delete_team" in request.POST:
            team_id = request.POST.get("team_id")
            team = get_object_or_404(Team, id=team_id, contest=contest)
            team.delete()
            messages.success(request, "Équipe supprimée.")

        return redirect("staff_admin:manage_teams", contest_id=contest_id)

    users = list(users_qs)
    teams = contest.teams.prefetch_related("members").all()
    teams_by_user = {user.id: user.teams.filter(contest=contest).exists() for user in users}

    return render(request, "staff_admin/manage_teams/manage_teams.html", {
        "contest": contest,
        "users": users,          # uniquement éligibles
        "teams": teams,
        "teams_by_user": teams_by_user,
    })
