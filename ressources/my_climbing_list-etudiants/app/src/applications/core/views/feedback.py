from applications.core.decorators import non_staff_required
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from applications.core.forms import FeedbackForm


@non_staff_required
def feedback_view(request):
    bloc = request.GET.get('bloc', 'false').lower() == 'true'  # Récupérer la discipline (bloc ou voie)
    success = None
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                # Récupérer les données du formulaire
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Construire le message email
                subject = f"Feedback de {name} via My Climbing List"
                full_message = f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}"
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = ['contact@example.test']

                # Envoyer l'email
                send_mail(subject, full_message, from_email, to_email)

                # Marquer le succès
                success = True
            except Exception as e:
                # En cas d'erreur, marquer l'échec
                success = False
        else:
            success = False

    return render(request, 'core/feedback/feedback.html', {
        'success': success,
        'bloc': bloc
    })
