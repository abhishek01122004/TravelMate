"""Trip ownership checks — use 404 for unauthorized access (no information leak)."""

from django.shortcuts import get_object_or_404

from .models import Trip


def trip_owned_or_404(trip_id, user):
    """
    Return the trip only if it belongs to the given user.
    Anonymous users should never reach here without @login_required.
    """
    return get_object_or_404(
        Trip.objects.select_related("destination")
                    .prefetch_related("bookings__hotel"),
        pk=trip_id,
        user=user,
    )
