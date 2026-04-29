from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from destinations.models import Destination

from .forms import TripForm
from .itinerary_logic import attractions_for_trip, build_day_plans
from .models import Trip
from .trip_access import trip_owned_or_404


@login_required
def create_trip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = Trip(
                user=request.user,
                destination=form.cleaned_data["destination"],
                budget=form.cleaned_data["budget"],
                num_people=form.cleaned_data["num_people"],
                trip_type=form.cleaned_data["trip_type"],
                start_date=form.cleaned_data["start_date"],
                end_date=form.cleaned_data["end_date"],
            )
            trip.save()  # save() auto-computes days from dates
            return redirect("itinerary", trip_id=trip.id)
    else:
        form = TripForm()

    return render(request, "planner/create_trip.html", {"form": form})


@login_required
def itinerary_view(request, trip_id):
    trip = trip_owned_or_404(trip_id, request.user)
    attractions = attractions_for_trip(trip)
    day_plans, remaining_budget, skipped_attractions = build_day_plans(trip, attractions)

    # Deduct hotel costs from remaining budget
    hotel_cost = sum(int(b.total_price or 0) for b in trip.bookings.all())
    remaining_budget -= hotel_cost

    context = {
        "trip": trip,
        "destination": trip.destination,
        "day_plans": day_plans,
        "remaining_budget": remaining_budget,
        "skipped_attractions": skipped_attractions,
    }
    return render(request, "planner/itinerary.html", context)


@login_required
def customize_itinerary(request, trip_id):
    trip = trip_owned_or_404(trip_id, request.user)
    all_attractions = list(
        trip.destination.attractions.all().order_by("name")
    )

    if request.method == "POST":
        raw_ids = request.POST.getlist("attractions")
        ids = []
        for x in raw_ids:
            s = str(x).strip()
            if s.isdigit():
                ids.append(int(s))
        trip.custom_attraction_ids = ids
        trip.save(update_fields=["custom_attraction_ids"])
        return redirect("itinerary", trip_id=trip.id)

    if trip.custom_attraction_ids is not None:
        selected_set = set()
        for x in trip.custom_attraction_ids:
            try:
                selected_set.add(int(x))
            except (TypeError, ValueError):
                continue
    else:
        selected_set = {a.id for a in all_attractions}

    for attraction in all_attractions:
        attraction.is_selected = attraction.id in selected_set

    current = attractions_for_trip(trip)
    day_plans, remaining_budget, _ = build_day_plans(trip, current)
    
    # Deduct hotel costs from remaining budget
    hotel_cost = sum(int(b.total_price or 0) for b in trip.bookings.all())
    remaining_budget -= hotel_cost

    context = {
        "trip": trip,
        "destination": trip.destination,
        "all_attractions": all_attractions,
        "day_plans": day_plans,
        "remaining_budget": remaining_budget,
    }
    return render(request, "planner/customize.html", context)


@login_required
@require_POST
def delete_trip(request, trip_id):
    from django.db import transaction
    from hotels.models import Room, Booking
    from django.contrib import messages
    
    trip = trip_owned_or_404(trip_id, request.user)
    
    try:
        with transaction.atomic():
            # Restore room inventory for any active bookings
            active_bookings = trip.bookings.filter(
                status__in=[Booking.STATUS_PENDING, Booking.STATUS_APPROVED]
            )
            for booking in active_bookings:
                room = Room.objects.select_for_update().get(id=booking.room_id)
                room.available_rooms += 1
                room.save(update_fields=["available_rooms"])
            
            # Delete the trip (this cascades and deletes the booking records too)
            trip.delete()
            messages.success(request, f"Trip to {trip.destination.name} has been deleted.")
    except Exception as e:
        messages.error(request, "An error occurred while deleting the trip.")
        
    return redirect("travel_profile")
