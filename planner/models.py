from django.conf import settings
from django.db import models

from destinations.models import Destination


from django.core.exceptions import ValidationError

class Trip(models.Model):
    TRIP_TYPE_CHOICES = [
        ("Solo", "Solo"),
        ("Friends", "Friends"),
        ("Family", "Family"),
        ("Romantic", "Romantic"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips",
        null=True,
        blank=True,
    )
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    
    # Deprecated manual input, now auto-computed from dates
    days = models.IntegerField(null=True, blank=True)
    
    budget = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # If set, itinerary uses only these attraction IDs (customize flow); empty list = use all
    custom_attraction_ids = models.JSONField(null=True, blank=True)

    # New fields
    num_people = models.IntegerField(null=True, blank=True)
    trip_type = models.CharField(
        max_length=20, 
        choices=TRIP_TYPE_CHOICES, 
        null=True, 
        blank=True
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after start date.")

    def save(self, *args, **kwargs):
        # Auto-compute days if dates are provided
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.days = max(1, delta.days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.destination.name} - {self.days} days"
