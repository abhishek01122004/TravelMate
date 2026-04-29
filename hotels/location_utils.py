"""
Location utilities for hotel proximity calculations.
Distance calculation is provided by destinations.geo_utils (single source of truth).
"""

from destinations.geo_utils import haversine_km  # noqa: F401 — re-exported for callers


def get_hotel_proximity(hotel, attractions):
    """
    Given a Hotel instance and a list of Attraction instances,
    return a dict with:
        - nearest_name  : name of the closest attraction (str or None)
        - nearest_km    : distance to the closest attraction (float or None)
        - avg_km        : average distance to all attractions that have coords (float or None)
        - label         : human-readable location quality label (str)

    If the hotel has no coordinates, or no attraction has coordinates,
    the distances will be None and the label will be "Location info not available".
    """
    # Hotel must have coordinates to calculate anything
    if hotel.latitude is None or hotel.longitude is None:
        return {
            "nearest_name": None,
            "nearest_km": None,
            "avg_km": None,
            "label": "Location info not available",
        }

    distances = []
    for attraction in attractions:
        if attraction.latitude is None or attraction.longitude is None:
            continue  # skip attractions without coordinates
        km = haversine_km(
            hotel.latitude, hotel.longitude,
            attraction.latitude, attraction.longitude,
        )
        distances.append((attraction.name, km))

    if not distances:
        return {
            "nearest_name": None,
            "nearest_km": None,
            "avg_km": None,
            "label": "Location info not available",
        }

    # Sort by distance to find the nearest
    distances.sort(key=lambda x: x[1])
    nearest_name, nearest_km = distances[0]
    avg_km = sum(d for _, d in distances) / len(distances)

    # Simple label based on average distance
    if avg_km < 2:
        label = "Excellent location"
    elif avg_km < 5:
        label = "Good location"
    else:
        label = "Moderate distance"

    return {
        "nearest_name": nearest_name,
        "nearest_km": round(nearest_km, 1),
        "avg_km": round(avg_km, 1),
        "label": label,
    }
