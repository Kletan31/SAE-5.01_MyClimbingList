from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings


@login_required
def delete_account_view(request):
    """
    Utilisation de "type: ignore" pour ne pas afficher les faux positifs que lève PyCharm concernant ces lignes.
    Le client est toujours authentifié grâce au décorateur "@login_required".
    """
    if request.method == "POST":
        username_confirmation = request.POST.get("username_confirmation")
        if username_confirmation == request.user.username:
            user = request.user
            user_email = user.email  # type: ignore
            user_username = user.username
            user.delete()

            # Envoi de l'email de confirmation
            send_mail(
                subject="Confirmation de suppression de votre compte",
                message=f"Bonjour {user_username},\n\nNous vous confirmons que votre compte a bien été supprimé de la "
                        f"plateforme My Climbing List.\n\nMerci pour votre confiance,\nAltissimo",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )

            return redirect('custom_auth:logout')
        else:
            return redirect("core:profile")
    return redirect("core:profile")
