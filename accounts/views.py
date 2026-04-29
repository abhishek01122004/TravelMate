from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import redirect, render

from hotels.location_utils import get_hotel_proximity
from hotels.models import Booking
from planner.itinerary_logic import attractions_for_trip, build_day_plans
from planner.models import Trip

from .forms import SignUpForm
from .models import Profile


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Update or create the profile with extra fields
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.age = form.cleaned_data.get('age')
            profile.city = form.cleaned_data.get('city')
            profile.address = form.cleaned_data.get('address')
            profile.phone_number = form.cleaned_data.get('phone_number')
            
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                
            profile.save()
            
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def travel_profile(request):
    """
    Trip dashboard: one card per trip with itinerary summary,
    hotel bookings (with proximity labels), and a cost summary.
    """
    booking_qs = (
        Booking.objects.select_related("hotel", "room")
        .order_by("check_in", "id")
    )

    trips = (
        Trip.objects.filter(user=request.user)
        .select_related("destination")
        .prefetch_related(
            Prefetch("bookings", queryset=booking_qs),
            "destination__attractions",  # for attractions_for_trip() — avoids 1 query per trip
        )
        .order_by("-created_at")
    )

    trip_cards = []
    for trip in trips:
        attractions = attractions_for_trip(trip)
        day_plans, remaining_budget, _ = build_day_plans(trip, attractions)

        budget_total = int(trip.budget or 0)
        scheduled_spend = budget_total - remaining_budget
        total_stops = sum(1 for day in day_plans for step in day.get("steps", []) if step.get("type") == "attraction")

        # --- proximity: cache per hotel so we don't recalculate for each booking ---
        proximity_cache = {}
        bookings_with_proximity = []
        hotel_cost = 0

        for booking in trip.bookings.all():
            hotel = booking.hotel
            if hotel.id not in proximity_cache:
                proximity_cache[hotel.id] = get_hotel_proximity(hotel, attractions)
            bookings_with_proximity.append({
                "booking": booking,
                "proximity": proximity_cache[hotel.id],
            })
            hotel_cost += int(booking.total_price or 0)

        grand_total = scheduled_spend + hotel_cost
        final_remaining_budget = remaining_budget - hotel_cost

        trip_cards.append({
            "trip": trip,
            "day_plans": day_plans,
            "remaining_budget": final_remaining_budget,
            "scheduled_spend": scheduled_spend,
            "total_stops": total_stops,
            "bookings_with_proximity": bookings_with_proximity,
            "hotel_cost": hotel_cost,
            "grand_total": grand_total,
        })

    return render(
        request,
        "accounts/travel_profile.html",
        {"trip_cards": trip_cards},
    )
