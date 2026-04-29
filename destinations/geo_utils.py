"""
Shared geographic utilities used across the project.
Both `hotels` and `planner` import from here — do not duplicate this logic.
"""
import math

# ---------------------------------------------------------------------------
# Travel assumptions used by the itinerary planner
# ---------------------------------------------------------------------------
TRAVEL_SPEED_KMH = 30      # Average urban travel speed (km/h)
TRAVEL_COST_PER_KM = 12    # Approximate taxi/auto fare (₹ per km)
MAX_HOURS_PER_DAY = 8      # Maximum scheduled activity hours per day


def haversine_km(lat1, lon1, lat2, lon2):
    """
    Return the great-circle distance in kilometres between two points
    given as (latitude, longitude) in decimal degrees.
    Uses the Haversine formula — accurate to ~0.5 % for city-scale distances.
    Returns 0.0 if any coordinate is None.
    """
    if None in (lat1, lon1, lat2, lon2):
        return 0.0

    R = 6371  # Earth's mean radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
