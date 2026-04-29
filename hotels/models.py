from django.conf import settings
from django.db import models

from destinations.models import Destination


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="hotels",
    )
    description = models.TextField()
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_hotels",
    )

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
    )
    room_type = models.CharField(max_length=100)
    price_per_night = models.IntegerField()
    capacity = models.IntegerField()
    available_rooms = models.IntegerField()

    def __str__(self):
        return f"{self.room_type} @ {self.hotel.name}"


class Booking(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hotel_bookings",
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    total_price = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    trip = models.ForeignKey(
        "planner.Trip",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    def __str__(self):
        return f"{self.user} · {self.hotel} · {self.status}"


class BookingGuest(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="guests_details"
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.age})"
