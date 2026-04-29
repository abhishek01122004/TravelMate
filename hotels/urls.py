from django.urls import path

from . import views

urlpatterns = [
    path("trip/<int:trip_id>/hotels/", views.trip_hotel_search, name="trip_hotel_search"),
    path(
        "trip/<int:trip_id>/book/<int:room_id>/",
        views.trip_room_book,
        name="trip_room_book",
    ),
    path("manager/", views.manager_hotel_list, name="manager_hotel_list"),
    path("manager/hotels/add/", views.manager_hotel_add, name="manager_hotel_add"),
    path(
        "manager/hotels/<int:hotel_id>/rooms/add/",
        views.manager_room_add,
        name="manager_room_add",
    ),
    path("manager/bookings/", views.manager_booking_list, name="manager_booking_list"),
    path(
        "manager/bookings/<int:booking_id>/approve/",
        views.manager_booking_approve,
        name="manager_booking_approve",
    ),
    path(
        "manager/bookings/<int:booking_id>/reject/",
        views.manager_booking_reject,
        name="manager_booking_reject",
    ),
]
