import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from planner.itinerary_logic import attractions_for_trip
from planner.trip_access import trip_owned_or_404

from .location_utils import get_hotel_proximity

from .booking_services import hotel_nights_exceed_trip_days, validate_booking_request
from .decorators import hotel_manager_required
from .forms import HotelForm, RoomForm, TripStaySearchForm
from .models import Booking, Hotel, Room

logger = logging.getLogger(__name__)


@login_required
@hotel_manager_required
def manager_hotel_list(request):
    hotels = (
        Hotel.objects.filter(owner=request.user)
        .select_related("destination")
        .prefetch_related("rooms")
        .order_by("name")
    )
    return render(
        request,
        "hotels/manager_hotel_list.html",
        {"hotels": hotels},
    )


@login_required
@hotel_manager_required
def manager_hotel_add(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, "Hotel added.")
            return redirect("manager_hotel_list")
    else:
        form = HotelForm()
    return render(
        request,
        "hotels/manager_hotel_form.html",
        {"form": form, "title": "Add hotel"},
    )


@login_required
@hotel_manager_required
def manager_room_add(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            messages.success(request, "Room added.")
            return redirect("manager_hotel_list")
    else:
        form = RoomForm()
    return render(
        request,
        "hotels/manager_room_form.html",
        {"form": form, "hotel": hotel},
    )


@login_required
@hotel_manager_required
def manager_booking_list(request):
    bookings = (
        Booking.objects.filter(hotel__owner=request.user)
        .select_related("user", "hotel", "room", "trip", "trip__destination")
        .order_by("check_in", "id")
    )
    return render(
        request,
        "hotels/manager_bookings.html",
        {"bookings": bookings},
    )


@login_required
@hotel_manager_required
@require_POST
def manager_booking_approve(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("hotel"),
        id=booking_id,
        hotel__owner=request.user,
    )
    if booking.status != Booking.STATUS_PENDING:
        messages.warning(request, "Only pending bookings can be approved.")
    else:
        booking.status = Booking.STATUS_APPROVED
        booking.save(update_fields=["status"])
        messages.success(request, "Booking approved.")
    return redirect("manager_booking_list")


@login_required
@hotel_manager_required
@require_POST
def manager_booking_reject(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("hotel", "room"),
        id=booking_id,
        hotel__owner=request.user,
    )
    if booking.status != Booking.STATUS_PENDING:
        messages.warning(request, "Only pending bookings can be rejected.")
    else:
        # Pending bookings already decremented inventory; restore on reject.
        with transaction.atomic():
            room = Room.objects.select_for_update().get(pk=booking.room_id)
            room.available_rooms += 1
            room.save(update_fields=["available_rooms"])
            booking.status = Booking.STATUS_REJECTED
            booking.save(update_fields=["status"])
        messages.success(request, "Booking rejected. Room availability restored.")
    return redirect("manager_booking_list")


@login_required
def trip_hotel_search(request, trip_id):
    trip = trip_owned_or_404(trip_id, request.user)
    rooms_with_meta = []
    searched_ok = False
    search_ctx = {}
    stay_exceeds_trip_days = False

    import datetime
    check_in = trip.start_date or datetime.date.today()
    check_out = trip.end_date or (check_in + datetime.timedelta(days=trip.days or 1))
    nights = max(1, (check_out - check_in).days)

    if request.method == "POST":
        form = TripStaySearchForm(request.POST)
        if form.is_valid():
            searched_ok = True
            guests = form.cleaned_data["guests"]

            stay_exceeds_trip_days = hotel_nights_exceed_trip_days(
                trip_days=trip.days, hotel_nights=nights
            )

            qs = (
                Room.objects.filter(
                    hotel__destination=trip.destination,
                    capacity__gte=guests,
                    available_rooms__gt=0,
                )
                .select_related("hotel")
                .order_by("hotel__name", "price_per_night")
            )

            # Fetch this trip's attractions once for proximity calculations
            trip_attractions = attractions_for_trip(trip)

            # Cache proximity per hotel so we don't recalculate for each room
            proximity_cache = {}

            for room in qs:
                hotel = room.hotel
                if hotel.id not in proximity_cache:
                    proximity_cache[hotel.id] = get_hotel_proximity(hotel, trip_attractions)

                rooms_with_meta.append(
                    {
                        "room": room,
                        "nights": nights,
                        "total_price": nights * room.price_per_night,
                        "proximity": proximity_cache[hotel.id],
                    }
                )
            search_ctx = {
                "search_guests": guests,
                "search_nights": nights,
                "search_check_in": check_in,
                "search_check_out": check_out,
            }
    else:
        initial_guests = trip.num_people if getattr(trip, 'num_people', None) else 2
        form = TripStaySearchForm(initial={'guests': initial_guests})

    context = {
        "trip": trip,
        "destination": trip.destination,
        "form": form,
        "rooms_with_meta": rooms_with_meta,
        "searched_ok": searched_ok,
        "stay_exceeds_trip_days": stay_exceeds_trip_days,
        "check_in_display": check_in.isoformat(),
        "check_out_display": check_out.isoformat(),
    }
    context.update(search_ctx)
    return render(request, "hotels/trip_hotels.html", context)


@login_required
def trip_room_book(request, trip_id, room_id):
    trip = trip_owned_or_404(trip_id, request.user)
    room = get_object_or_404(Room.objects.select_related("hotel"), id=room_id)

    # Determine number of guests
    try:
        if request.method == "POST":
            guests = int(request.POST.get("guests", 1))
        else:
            guests = int(request.GET.get("guests", 1))
    except ValueError:
        guests = 1

    from .forms import BookingGuestFormSet
    import datetime
    check_in = trip.start_date or datetime.date.today()
    check_out = trip.end_date or (check_in + datetime.timedelta(days=trip.days or 1))
    nights = max(1, (check_out - check_in).days)
    total_price = nights * room.price_per_night

    if request.method == "POST":
        formset = BookingGuestFormSet(request.POST, prefix='guests')
        if not formset.is_valid():
            messages.error(request, "Please fix the errors in the guest details form.")
        else:
            # Prevent duplicate bookings: one active booking per trip
            existing = trip.bookings.filter(
                status__in=[Booking.STATUS_PENDING, Booking.STATUS_APPROVED]
            ).first()
            if existing:
                messages.error(
                    request,
                    f"You already have an active booking at {existing.hotel.name} for this trip. "
                    "It must be rejected before you can request a different room.",
                )
                return redirect("trip_hotel_search", trip_id=trip.id)

            ok, err = validate_booking_request(
                room=room, trip=trip, guests=guests, check_in=check_in, check_out=check_out
            )
            if not ok:
                messages.error(request, err)
                return redirect("trip_hotel_search", trip_id=trip.id)

            if hotel_nights_exceed_trip_days(trip_days=trip.days, hotel_nights=nights):
                messages.warning(
                    request,
                    f"Note: your hotel stay ({nights} nights) is longer than your "
                    f"{trip.days}-day itinerary plan.",
                )

            try:
                with transaction.atomic():
                    room_locked = Room.objects.select_for_update().get(pk=room.id)
                    ok2, err2 = validate_booking_request(
                        room=room_locked,
                        trip=trip,
                        guests=guests,
                        check_in=check_in,
                        check_out=check_out,
                    )
                    if not ok2:
                        messages.error(request, err2)
                        return redirect("trip_hotel_search", trip_id=trip.id)

                    booking = Booking.objects.create(
                        user=request.user,
                        hotel=room_locked.hotel,
                        room=room_locked,
                        check_in=check_in,
                        check_out=check_out,
                        guests=guests,
                        total_price=total_price,
                        status=Booking.STATUS_PENDING,
                        trip=trip,
                    )
                    room_locked.available_rooms -= 1
                    room_locked.save(update_fields=["available_rooms"])

                    # Save guests
                    for form in formset:
                        if form.cleaned_data:
                            guest = form.save(commit=False)
                            guest.booking = booking
                            guest.save()

            except Exception:
                logger.exception(
                    "Booking failed — user=%s trip=%s room=%s",
                    request.user.id, trip.id, room_id,
                )
                messages.error(request, "Could not complete booking. Please try again.")
                return redirect("trip_hotel_search", trip_id=trip.id)

            messages.success(
                request,
                "Booking request sent. Total: "
                f"₹{total_price} for {nights} night(s). Awaiting hotel approval.",
            )
            return redirect("itinerary", trip_id=trip.id)
    else:
        # Pre-fill number of forms based on guests
        BookingGuestFormSet.extra = guests
        formset = BookingGuestFormSet(prefix='guests')

    context = {
        "trip": trip,
        "room": room,
        "guests": guests,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "total_price": total_price,
        "formset": formset,
    }
    return render(request, "hotels/trip_room_book.html", context)
