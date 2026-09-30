from django.shortcuts import render


def install_guide_view(request):
    return render(request, 'services/install_guide/install_guide.html')
