# applications/contest/utils/score_initialization.py

from applications.contest.models import Inscription
from applications.contest.utils.scoring import compute_user_score


def initialize_score_initial(inscription: Inscription) -> None:
    """
    Initialise score_initial une seule fois.
    """
    if inscription.score_initial is not None:
        return

    contest = inscription.contest
    user = inscription.user

    score_initial = 0
    source_contest = contest.initial_contest

    if source_contest:
        try:
            source_inscription = Inscription.objects.get(
                contest=source_contest,
                user=user,
            )

            if source_inscription.is_active():
                score_initial = compute_user_score(
                    contest=source_contest,
                    user_id=user.id,
                )

        except Inscription.DoesNotExist:
            pass

    inscription.score_initial = score_initial
    inscription.save(update_fields=["score_initial"])
