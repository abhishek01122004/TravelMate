from django import forms

from .models import Hotel, Room, BookingGuest


class TripStaySearchForm(forms.Form):
    guests = forms.IntegerField(
        min_value=1,
        initial=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        label="Number of guests",
    )


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ("name", "destination", "description", "address", "latitude", "longitude")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "destination": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. MG Road, Bengaluru, Karnataka 560001",
            }),
            "latitude": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 28.6139",
                "step": "any",
            }),
            "longitude": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 77.2090",
                "step": "any",
            }),
        }
        help_texts = {
            "address": "Full street address of the hotel.",
            "latitude": "Decimal latitude — right-click any location on Google Maps to copy coordinates.",
            "longitude": "Decimal longitude — paste the second number from Google Maps coordinates.",
        }

    def clean_latitude(self):
        lat = self.cleaned_data.get("latitude")
        if lat is not None and not (-90 <= lat <= 90):
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return lat

    def clean_longitude(self):
        lon = self.cleaned_data.get("longitude")
        if lon is not None and not (-180 <= lon <= 180):
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return lon


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("room_type", "price_per_night", "capacity", "available_rooms")
        widgets = {
            "room_type": forms.TextInput(attrs={"class": "form-control"}),
            "price_per_night": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "available_rooms": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def clean_price_per_night(self):
        price = self.cleaned_data.get("price_per_night")
        if price is not None and price < 0:
            raise forms.ValidationError("Price per night cannot be negative.")
        return price

    def clean_capacity(self):
        cap = self.cleaned_data.get("capacity")
        if cap is not None and cap < 1:
            raise forms.ValidationError("Capacity must be at least 1.")
        return cap

    def clean_available_rooms(self):
        avail = self.cleaned_data.get("available_rooms")
        if avail is not None and avail < 0:
            raise forms.ValidationError("Available rooms cannot be negative.")
        return avail


class BookingGuestForm(forms.ModelForm):
    class Meta:
        model = BookingGuest
        fields = ("name", "age", "gender")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guest Full Name"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 0, "placeholder": "Age"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
        }

BookingGuestFormSet = forms.formset_factory(
    BookingGuestForm,
    extra=1,
)

