import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from applications.core.models import Seance


@login_required
@require_POST
def project_refresh(request):
    try:
        data = json.loads(request.body)
        ouverture_id = data.get('ouverture_id')
        user = request.user

        Seance.objects.filter(user=user, ouverture_id=ouverture_id).update(is_project_visible=False)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
