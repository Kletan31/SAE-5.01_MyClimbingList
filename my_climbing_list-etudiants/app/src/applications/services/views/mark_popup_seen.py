from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from applications.core.models import MessagePopup, MessagePopupView


@require_POST
@login_required
def mark_popup_seen_view(request):
    popup = MessagePopup.objects.order_by('-created_at').first()
    if popup:
        MessagePopupView.objects.get_or_create(user=request.user, popup=popup)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
