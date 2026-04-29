"""Shared day-by-day itinerary builder (time + budget)."""

from destinations.geo_utils import (
    MAX_HOURS_PER_DAY,
    TRAVEL_COST_PER_KM,
    TRAVEL_SPEED_KMH,
    haversine_km,
)


def attractions_for_trip(trip):
    """Attractions for this trip, filtered by custom_attraction_ids when set."""
    qs = trip.destination.attractions.all().order_by(
        "-priority", "-estimated_time", "name"
    )
    if trip.custom_attraction_ids is not None:
        allowed = set()
        for x in trip.custom_attraction_ids:
            try:
                allowed.add(int(x))
            except (TypeError, ValueError):
                continue
        return [a for a in qs if a.id in allowed]
    return list(qs)


def _travel(dist_km):
    """Return (travel_time_hours, travel_cost_inr) for a given distance."""
    return dist_km / TRAVEL_SPEED_KMH, int(dist_km * TRAVEL_COST_PER_KM)


def build_day_plans(trip, attractions_list):
    """
    attractions_list: list of Attraction instances, already ordered by priority.
    Returns (day_plans, remaining_budget).
    """
    days = max(1, trip.days or 1)
    remaining_budget = int(trip.budget or 0)
    skipped_attractions = []  # attractions that couldn't be scheduled

    hotel_lat = hotel_lon = hotel_name = None

    # Resolve hotel coordinates — uses prefetch cache when available (avoids N+1)
    _bookings = list(trip.bookings.all())
    booking = _bookings[0] if _bookings else None
    if booking and booking.hotel:
        h = booking.hotel
        if h.latitude is not None and h.longitude is not None:
            hotel_lat, hotel_lon, hotel_name = h.latitude, h.longitude, h.name

    # ── Initialise day buckets ──────────────────────────────────────────────
    day_plans = [
        {
            "day": day,
            "steps": [],
            "hours": 0.0,
            "cost": 0,
            "total_attraction_time": 0.0,
            "total_travel_time": 0.0,
            "remaining_hours": float(MAX_HOURS_PER_DAY),
            "reserved_hotel_return_time": 0.0,
            "reserved_hotel_return_cost": 0,
        }
        for day in range(1, days + 1)
    ]

    remaining_attractions = list(attractions_list)

    def get_last_attraction(dp):
        for step in reversed(dp["steps"]):
            if step["type"] == "attraction":
                return step["data"]
        return None

    # ── Step 1: Distribute unique attractions across all days ───────────────
    for attraction in remaining_attractions:
        duration = max(0.0, float(attraction.estimated_time or 0))
        price = int(attraction.approx_cost or 0)

        valid_days = []
        for dp in day_plans:
            refund_time = dp["reserved_hotel_return_time"]
            refund_cost = dp["reserved_hotel_return_cost"]
            travel_time = travel_cost = 0.0
            new_reserved_time = new_reserved_cost = 0.0

            last_att = get_last_attraction(dp)
            if not last_att:
                if hotel_lat is not None:
                    d = haversine_km(hotel_lat, hotel_lon, attraction.latitude, attraction.longitude)
                    travel_time, travel_cost = _travel(d)
                    d2 = haversine_km(attraction.latitude, attraction.longitude, hotel_lat, hotel_lon)
                    new_reserved_time, new_reserved_cost = _travel(d2)
            else:
                d = haversine_km(last_att.latitude, last_att.longitude, attraction.latitude, attraction.longitude)
                travel_time, travel_cost = _travel(d)
                if hotel_lat is not None:
                    d2 = haversine_km(attraction.latitude, attraction.longitude, hotel_lat, hotel_lon)
                    new_reserved_time, new_reserved_cost = _travel(d2)

            net_time = travel_time + new_reserved_time - refund_time
            net_cost = travel_cost + new_reserved_cost - refund_cost

            if (dp["hours"] + duration + net_time <= MAX_HOURS_PER_DAY
                    and remaining_budget >= price + net_cost):
                valid_days.append((dp, travel_time, travel_cost,
                                   new_reserved_time, new_reserved_cost,
                                   refund_time, refund_cost, last_att))

        if not valid_days:
            skipped_attractions.append(attraction)
            continue

        best_day, travel_time, travel_cost, new_reserved_time, new_reserved_cost, refund_time, refund_cost, last_att = \
            min(valid_days, key=lambda x: x[0]["hours"])

        net_time = travel_time + new_reserved_time - refund_time
        net_cost = travel_cost + new_reserved_cost - refund_cost

        if last_att:
            best_day["steps"].append({
                "type": "travel",
                "travel_time": int(travel_time * 60),
                "travel_cost": int(travel_cost),
                "distance": round(d, 1),
                "from": last_att.name,
                "to": attraction.name,
            })

        best_day["steps"].append({"type": "attraction", "data": attraction})
        best_day["hours"] += duration + net_time
        best_day["cost"] += price + int(net_cost)
        best_day["total_attraction_time"] += duration
        best_day["total_travel_time"] += net_time
        best_day["remaining_hours"] -= duration + net_time
        best_day["reserved_hotel_return_time"] = new_reserved_time
        best_day["reserved_hotel_return_cost"] = new_reserved_cost
        remaining_budget -= price + int(net_cost)

    # ── Step 2: Fill slack time with low-priority attractions ───────────────
    low_priority_pool = [a for a in remaining_attractions if a.priority <= 3]

    for dp in day_plans:
        if dp["remaining_hours"] < 2.0:
            continue
        for attraction in low_priority_pool:
            already_in_day = any(
                s["type"] == "attraction" and s["data"] == attraction
                for s in dp["steps"]
            )
            if already_in_day:
                continue

            duration = max(0.0, float(attraction.estimated_time or 0))
            price = int(attraction.approx_cost or 0)
            refund_time = dp["reserved_hotel_return_time"]
            refund_cost = dp["reserved_hotel_return_cost"]
            travel_time = travel_cost = 0.0
            new_reserved_time = new_reserved_cost = 0.0

            last_att = get_last_attraction(dp)
            if not last_att:
                if hotel_lat is not None:
                    d = haversine_km(hotel_lat, hotel_lon, attraction.latitude, attraction.longitude)
                    travel_time, travel_cost = _travel(d)
                    d2 = haversine_km(attraction.latitude, attraction.longitude, hotel_lat, hotel_lon)
                    new_reserved_time, new_reserved_cost = _travel(d2)
            else:
                d = haversine_km(last_att.latitude, last_att.longitude, attraction.latitude, attraction.longitude)
                travel_time, travel_cost = _travel(d)
                if hotel_lat is not None:
                    d2 = haversine_km(attraction.latitude, attraction.longitude, hotel_lat, hotel_lon)
                    new_reserved_time, new_reserved_cost = _travel(d2)

            net_time = travel_time + new_reserved_time - refund_time
            net_cost = travel_cost + new_reserved_cost - refund_cost

            if (dp["remaining_hours"] >= duration + net_time
                    and remaining_budget >= price + net_cost):
                if last_att:
                    dp["steps"].append({
                        "type": "travel",
                        "travel_time": int(travel_time * 60),
                        "travel_cost": int(travel_cost),
                        "distance": round(d, 1),
                        "from": last_att.name,
                        "to": attraction.name,
                    })
                dp["steps"].append({"type": "attraction", "data": attraction})
                dp["hours"] += duration + net_time
                dp["cost"] += price + int(net_cost)
                dp["total_attraction_time"] += duration
                dp["total_travel_time"] += net_time
                dp["remaining_hours"] -= duration + net_time
                dp["reserved_hotel_return_time"] = new_reserved_time
                dp["reserved_hotel_return_cost"] = new_reserved_cost
                remaining_budget -= price + int(net_cost)

                if dp["remaining_hours"] < 2.0:
                    break

    # ── Step 3: Prepend/append hotel↔attraction travel legs ────────────────
    for dp in day_plans:
        if dp["steps"] and hotel_lat is not None:
            first_att = next(
                (s["data"] for s in dp["steps"] if s["type"] == "attraction"), None
            )
            last_att = get_last_attraction(dp)

            if first_att:
                d = haversine_km(hotel_lat, hotel_lon, first_att.latitude, first_att.longitude)
                t, c = _travel(d)
                dp["steps"].insert(0, {
                    "type": "travel",
                    "travel_time": int(t * 60),
                    "travel_cost": int(c),
                    "distance": round(d, 1),
                    "from": hotel_name,
                    "to": first_att.name,
                })

            if last_att:
                d = haversine_km(last_att.latitude, last_att.longitude, hotel_lat, hotel_lon)
                t, c = _travel(d)
                dp["steps"].append({
                    "type": "travel",
                    "travel_time": int(t * 60),
                    "travel_cost": int(c),
                    "distance": round(d, 1),
                    "from": last_att.name,
                    "to": hotel_name,
                })

        dp.pop("reserved_hotel_return_time", None)
        dp.pop("reserved_hotel_return_cost", None)
        dp["hours"] = round(dp["hours"], 1)
        dp["total_travel_time"] = round(dp["total_travel_time"], 1)

    return day_plans, remaining_budget, skipped_attractions
