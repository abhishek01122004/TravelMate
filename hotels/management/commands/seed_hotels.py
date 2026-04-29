import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from destinations.models import Destination, Attraction
from hotels.models import Hotel, Room

class Command(BaseCommand):
    help = 'Seeds the database with hotels and rooms for existing destinations.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        
        # Ensure we have at least one user to own the hotels
        owner_user = User.objects.first()
        if not owner_user:
            owner_user = User.objects.create_user(
                username='hotel_manager_seed',
                password='seedpassword123'
            )
            self.stdout.write(self.style.WARNING("Created dummy user 'hotel_manager_seed' to own hotels."))

        destinations = Destination.objects.prefetch_related('attractions')
        
        if not destinations.exists():
            self.stdout.write(self.style.ERROR("No destinations found. Please run seed_travel_data first."))
            return

        hotel_prefixes = ["Grand", "Royal", "The", "Comfort Inn", "Regency", "Palace", "Sunset", "Premium"]
        hotel_suffixes = ["Residency", "Hotel", "Resort", "Inn", "Suites", "Retreat"]
        
        room_types_data = [
            {"type": "Standard", "price_min": 1500, "price_max": 3500, "capacity": 2},
            {"type": "Deluxe", "price_min": 3500, "price_max": 6500, "capacity": 3},
            {"type": "Suite", "price_min": 7000, "price_max": 12000, "capacity": 4},
            {"type": "Family Room", "price_min": 5000, "price_max": 8000, "capacity": 5},
        ]

        total_hotels_created = 0
        total_rooms_created = 0

        with transaction.atomic():
            for destination in destinations:
                attractions = list(destination.attractions.all())
                
                # Base coordinates on the first attraction if available, else use a default
                base_lat = attractions[0].latitude if attractions and attractions[0].latitude else 20.0
                base_lon = attractions[0].longitude if attractions and attractions[0].longitude else 78.0

                num_hotels = random.randint(3, 5)
                
                for i in range(num_hotels):
                    hotel_name = f"{random.choice(hotel_prefixes)} {destination.name} {random.choice(hotel_suffixes)}"
                    
                    # Avoid duplicates
                    if Hotel.objects.filter(name=hotel_name, destination=destination).exists():
                        continue
                        
                    # Add small random offset to coordinates (approx 0 to 5 km)
                    lat_offset = random.uniform(-0.04, 0.04)
                    lon_offset = random.uniform(-0.04, 0.04)
                    
                    hotel = Hotel.objects.create(
                        name=hotel_name,
                        destination=destination,
                        description=f"A wonderful {hotel_name} located in the heart of {destination.name}, offering premium amenities and great comfort.",
                        address=f"Near Main Road, {destination.name}",
                        latitude=base_lat + lat_offset,
                        longitude=base_lon + lon_offset,
                        owner=owner_user
                    )
                    total_hotels_created += 1
                    
                    # Create rooms for this hotel
                    num_room_types = random.randint(2, 3)
                    selected_room_types = random.sample(room_types_data, num_room_types)
                    
                    rooms_to_create = []
                    for rt in selected_room_types:
                        # Ensure we don't recreate the same room type for the same hotel
                        if not Room.objects.filter(hotel=hotel, room_type=rt["type"]).exists():
                            rooms_to_create.append(
                                Room(
                                    hotel=hotel,
                                    room_type=rt["type"],
                                    price_per_night=random.randint(rt["price_min"], rt["price_max"]) // 100 * 100, # Round to nearest 100
                                    capacity=rt["capacity"],
                                    available_rooms=random.randint(5, 20)
                                )
                            )
                            
                    if rooms_to_create:
                        Room.objects.bulk_create(rooms_to_create)
                        total_rooms_created += len(rooms_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully processed destinations. Created {total_hotels_created} new hotels and {total_rooms_created} new rooms."))
