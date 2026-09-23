from applications.core.decorators import non_staff_required
from django.shortcuts import render
from applications.core.utils import get_user_projects


@non_staff_required
def projects_view(request):
    projets = get_user_projects(request.user)

    # Trier par niveau décroissant (le niveau est une chaîne, donc tri alphabétique inversé fonctionne)
    projets = sorted(projets, key=lambda p: p['niveau'], reverse=True)

    # Séparer voies et blocs
    projets_voie = []
    projets_bloc = []

    for projet in projets:
        if projet['bloc']:
            projets_bloc.append(projet)
        else:
            projets_voie.append(projet)

    return render(request, 'core/projects/projects.html', {
        'projets_voie': projets_voie,
        'projets_bloc': projets_bloc
    })
