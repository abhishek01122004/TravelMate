from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_trip, name="create_trip"),
    path("itinerary/<int:trip_id>/", views.itinerary_view, name="itinerary"),
    path(
        "itinerary/<int:trip_id>/customize/",
        views.customize_itinerary,
        name="customize_itinerary",
    ),
    path("trip/<int:trip_id>/delete/", views.delete_trip, name="delete_trip"),
]

