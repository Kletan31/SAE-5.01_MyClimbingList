from .public import event_home, event_register
from .team_access import team_access
from .auth import staff_login, staff_logout
from .routes import (
    staff_route_list,
    staff_delete_route,
    staff_move_route_up,
    staff_move_route_down,
    staff_toggle_route_zone,
)
from .staff import (
    staff_home,
    staff_team_list,
    staff_validate_team,
    staff_unvalidate_team,
    staff_delete_team,
    staff_resend_team_link,
    staff_team_update,
)
from .ranking import (
    team_ranking,
    staff_ranking,
    staff_ranking_display,
    public_ranking,
)
from .events import (
    staff_event_list,
    staff_event_create,
    staff_event_update,
    staff_event_delete,
    staff_phase_create,
    staff_phase_delete,
    staff_phase_update,
)