"""
Validation helpers for traveler hotel booking (no calendar overlap logic).
"""


def validate_booking_request(*, room, trip, guests, check_in, check_out):
    """
    Return (ok: bool, error_message: str | None).
    Caller must hold no DB locks; use inside transaction after select_for_update for inventory.
    """
    if check_out <= check_in:
        return False, "Check-out must be after check-in."

    nights = (check_out - check_in).days
    if nights < 1:
        return False, "Stay must be at least one night."

    if room.hotel.destination_id != trip.destination_id:
        return False, "That room is not available for this trip’s destination."

    if guests > room.capacity:
        return False, "This room does not fit your guest count."

    if room.available_rooms <= 0:
        return False, "This room is no longer available."

    return True, None


def hotel_nights_exceed_trip_days(*, trip_days: int, hotel_nights: int) -> bool:
    """True if the hotel stay is longer than the planned itinerary day count (UX warning only)."""
    return hotel_nights > max(1, trip_days)
