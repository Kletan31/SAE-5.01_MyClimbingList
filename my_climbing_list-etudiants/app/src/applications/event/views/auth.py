from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse


def staff_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        next_url = request.GET.get("next")
        return redirect(next_url or reverse("event:staff_home"))

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        if not user.is_staff:
            form.add_error(None, "Cet espace est réservé au staff.")
        else:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next")
            return redirect(next_url or reverse("event:staff_home"))

    return render(
        request,
        "event/staff/login.html",
        {
            "form": form,
            "next": request.GET.get("next", ""),
        },
    )


def staff_logout(request):
    logout(request)
    return redirect("event:staff_login")