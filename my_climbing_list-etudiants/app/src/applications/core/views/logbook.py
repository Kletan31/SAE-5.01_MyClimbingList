from django.shortcuts import render
from applications.core.decorators import non_staff_required
from applications.core.utils import get_routes_data


@non_staff_required
def logbook_view(request):
    user = request.user
    bloc = request.GET.get('bloc', 'false').lower() == 'true'

    modes = request.GET.getlist('mode')  # ex: ['flash'], ['lead'], ['flash', 'lead']
    flashed = 'flash' in modes
    leaded = 'lead' in modes

    logbook = get_routes_data(user, bloc, flashed, leaded)

    return render(request, 'core/logbook/logbook.html', {
        'logbook': logbook,
        'bloc': bloc,
        'flashed': flashed,
        'leaded': leaded,
    })
