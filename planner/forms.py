import datetime

from django import forms

from destinations.models import Destination

from .models import Trip


class TripForm(forms.Form):
    destination = forms.ModelChoiceField(
        queryset=Destination.objects.all().order_by("name"),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-select", "id": "destination"}),
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control", "id": "start_date"}
        ),
        label="Start Date",
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control", "id": "end_date"}
        ),
        label="End Date",
    )
    num_people = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1, "id": "num_people"}
        ),
        label="Number of People",
    )
    trip_type = forms.ChoiceField(
        choices=[("", "Select...")] + list(Trip.TRIP_TYPE_CHOICES),
        widget=forms.Select(attrs={"class": "form-select", "id": "trip_type"}),
        label="Trip Type",
    )
    budget = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 0, "id": "budget"}
        ),
        label="Budget",
    )

    def clean_trip_type(self):
        value = self.cleaned_data.get("trip_type")
        if not value:
            raise forms.ValidationError("Please select a trip type.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        
        if start_date and start_date < datetime.date.today():
            self.add_error("start_date", "Start date cannot be in the past.")
            
        if start_date and end_date:
            if end_date <= start_date:
                self.add_error("end_date", "End date must be after start date.")
                
        return cleaned_data
