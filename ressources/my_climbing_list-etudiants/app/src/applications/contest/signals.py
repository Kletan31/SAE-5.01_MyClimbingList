# applications/contest/signals.py

from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Inscription, Team


def _purge_user_from_teams(contest, user):
    # Retire l'utilisateur de toutes les équipes du contest (idempotent)
    for team in Team.objects.filter(contest=contest, members=user).only("id"):
        team.members.remove(user)


@receiver(post_save, sender=Inscription)
def enforce_team_membership_on_status_change(sender, instance: Inscription, created, **kwargs):
    contest = instance.contest
    if not contest.is_team_contest:
        return

    # Si refusé -> purge des équipes
    if instance.status == Inscription.Status.REFUSED:
        transaction.on_commit(lambda: _purge_user_from_teams(contest, instance.user))


@receiver(post_delete, sender=Inscription)
def enforce_team_membership_on_delete(sender, instance: Inscription, **kwargs):
    contest = instance.contest
    if not contest.is_team_contest:
        return
    transaction.on_commit(lambda: _purge_user_from_teams(contest, instance.user))
