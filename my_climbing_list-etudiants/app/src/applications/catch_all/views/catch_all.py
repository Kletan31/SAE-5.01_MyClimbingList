# Redirection vers une page générique (logo Altissimo)
# from django.shortcuts import render
#
#
# def catch_all_view(request, *args, **kwargs):
#     return render(request, 'catch_all/catch_all.html', {})


# Redirection vers la page d'accueil (home ou login selon l'état de connexion du client)
from django.shortcuts import redirect


def catch_all_view(request, *args, **kwargs):
    return redirect('core:home')
