from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from applications.core.models import Ouverture
from applications.route_event.decorators import route_event_staff_required
from applications.route_event.models import RouteEventRoute
from applications.route_event.permissions import (
    get_staff_event_or_404,
    get_staff_salle,
)


def is_fetch_request(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def redirect_to_route_list(event_slug, route_id=None):
    url = reverse("route_event:staff_route_list", kwargs={"slug": event_slug})

    if route_id:
        return redirect(f"{url}#route-{route_id}")

    return redirect(url)


@route_event_staff_required
def staff_route_list(request, slug):
    event = get_staff_event_or_404(request, slug)

    routes = (
        RouteEventRoute.objects
        .select_related("ouverture")
        .filter(event=event)
        .order_by("display_order", "ouverture__relais", "ouverture__id")
    )

    already_added_ids = routes.values_list("ouverture_id", flat=True)

    available_routes = (
        Ouverture.objects
        .filter(
            salle=event.salle,
            bloc=False,
            active=True,
        )
        .exclude(id__in=already_added_ids)
        .order_by("relais", "niveau", "couleur")
    )

    if request.method == "POST":
        selected_ids = request.POST.getlist("ouvertures")

        if selected_ids:
            current_max_order = (
                RouteEventRoute.objects
                .filter(event=event)
                .aggregate(Max("display_order"))["display_order__max"]
            )

            current_max_order = current_max_order or 0

            for ouverture_id in selected_ids:
                current_max_order += 1

                RouteEventRoute.objects.create(
                    event=event,
                    ouverture_id=ouverture_id,
                    display_order=current_max_order,
                )

            return redirect("route_event:staff_route_list", slug=event.slug)

    return render(
        request,
        "route_event/staff/route_list.html",
        {
            "event": event,
            "routes": routes,
            "available_routes": available_routes,
        },
    )


@route_event_staff_required
def staff_delete_route(request, route_id):
    event_route = get_object_or_404(
        RouteEventRoute.objects.select_related("event"),
        pk=route_id,
        event__salle=get_staff_salle(request),
    )

    if request.method == "POST":
        event_slug = event_route.event.slug
        event_route.delete()

        return redirect_to_route_list(event_slug)

    return redirect_to_route_list(event_route.event.slug, event_route.id)


def swap_route_orders(current_route, other_route):
    current_order = current_route.display_order
    other_order = other_route.display_order

    temp_order = (
        RouteEventRoute.objects
        .filter(event=current_route.event)
        .aggregate(Max("display_order"))["display_order__max"]
        or 0
    ) + 1

    current_route.display_order = temp_order
    current_route.save()

    other_route.display_order = current_order
    other_route.save()

    current_route.display_order = other_order
    current_route.save()

    return {
        "moved_route_id": current_route.id,
        "swapped_route_id": other_route.id,
        "moved_order": current_route.display_order,
        "swapped_order": other_route.display_order,
    }


@route_event_staff_required
def staff_move_route_up(request, route_id):
    current_route = get_object_or_404(
        RouteEventRoute.objects.select_related("event"),
        pk=route_id,
        event__salle=get_staff_salle(request),
    )

    previous_route = (
        RouteEventRoute.objects
        .filter(
            event=current_route.event,
            display_order__lt=current_route.display_order,
        )
        .order_by("-display_order")
        .first()
    )

    if not previous_route:
        if is_fetch_request(request):
            return JsonResponse({"moved": False})

        return redirect_to_route_list(current_route.event.slug, current_route.id)

    swap_data = swap_route_orders(current_route, previous_route)

    if is_fetch_request(request):
        return JsonResponse(
            {
                "moved": True,
                "direction": "up",
                **swap_data,
            }
        )

    return redirect_to_route_list(current_route.event.slug, current_route.id)


@route_event_staff_required
def staff_move_route_down(request, route_id):
    current_route = get_object_or_404(
        RouteEventRoute.objects.select_related("event"),
        pk=route_id,
        event__salle=get_staff_salle(request),
    )

    next_route = (
        RouteEventRoute.objects
        .filter(
            event=current_route.event,
            display_order__gt=current_route.display_order,
        )
        .order_by("display_order")
        .first()
    )

    if not next_route:
        if is_fetch_request(request):
            return JsonResponse({"moved": False})

        return redirect_to_route_list(current_route.event.slug, current_route.id)

    swap_data = swap_route_orders(current_route, next_route)

    if is_fetch_request(request):
        return JsonResponse(
            {
                "moved": True,
                "direction": "down",
                **swap_data,
            }
        )

    return redirect_to_route_list(current_route.event.slug, current_route.id)