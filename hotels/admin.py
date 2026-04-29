from django.contrib import admin

from .models import Booking, Hotel, Room


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "owner")
    list_filter = ("destination",)
    search_fields = ("name",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_type", "hotel", "price_per_night", "capacity", "available_rooms")
    list_filter = ("hotel",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "trip",
        "hotel",
        "room",
        "check_in",
        "check_out",
        "guests",
        "total_price",
        "status",
    )
    list_filter = ("status", "hotel")
