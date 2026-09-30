# applications/core/views/settings.py

from applications.core.validators import validate_email, validate_username, validate_name, validate_gender
from django.shortcuts import render
from applications.core.decorators import non_staff_required


@non_staff_required
def settings_view(request):
    """
    Utilisation de "type: ignore" pour ne pas afficher les faux positifs que lève PyCharm concernant ces lignes.
    Le client est toujours authentifié grâce au décorateur "@non_staff_required".
    """
    user = request.user
    profile = user.profile  # type: ignore
    bloc = request.GET.get('bloc', 'false').lower() == 'true'  # Récupérer la discipline (bloc ou voie)

    context = {
        'user': user,
        'profile': profile,
        'bloc': bloc,
    }

    if request.method == 'POST':
        # Récupérer les données envoyées
        form_data = {
            'email': request.POST.get('email', '').strip(),
            'username': request.POST.get('username', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'first_name': request.POST.get('first_name', '').strip(),
            'gender': request.POST.get('gender', '').strip(),
        }

        # Définir les champs et leurs validations
        validations = {
            'email': (user.email, validate_email),              # type: ignore
            'username': (user.username, validate_username),
            'first_name': (user.first_name, validate_name),     # type: ignore
            'last_name': (user.last_name, validate_name),       # type: ignore
            'gender': (profile.gender, validate_gender),
        }

        # Parcourir chaque champ pour valider et mettre à jour si nécessaire
        for field, (current_value, validator) in validations.items():
            new_value = form_data[field]
            if new_value != current_value:  # Vérifier si le champ a changé
                is_valid, error_message = validator(new_value)
                if not is_valid:  # Validation échouée
                    context['error'] = error_message
                    return render(request, 'core/settings/settings.html', context)

                # Mettre à jour les données utilisateur ou profil
                if field == 'gender':
                    setattr(profile, field, new_value)  # Mise à jour du profil
                else:
                    setattr(user, field, new_value)  # Mise à jour de l'utilisateur

        # Sauvegarder les modifications
        user.save()
        profile.save()
        context['success'] = 'Modifications prises en compte'  # type: ignore

        return render(request, 'core/settings/settings.html', context)

    # Si la méthode n'est pas POST, affichage des données
    return render(request, 'core/settings/settings.html', context)
