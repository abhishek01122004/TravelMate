from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_TRAVELER = "user"
    ROLE_HOTEL_MANAGER = "hotel_manager"

    ROLE_CHOICES = [
        (ROLE_TRAVELER, "Traveler"),
        (ROLE_HOTEL_MANAGER, "Hotel Manager"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_TRAVELER)

    # Additional profile details
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
