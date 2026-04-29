from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from accounts.models import Profile
from hotels.models import Hotel

class Command(BaseCommand):
    help = 'Assigns abhishek1 as Hotel Manager and links all existing hotels to this user.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        target_username = "abhishek1"
        
        # Get or create the user
        try:
            user = User.objects.get(username=target_username)
            self.stdout.write(f"Found user '{target_username}'.")
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"User '{target_username}' not found. Creating user..."))
            user = User.objects.create_user(username=target_username, password="password123")
            self.stdout.write(self.style.SUCCESS(f"Created user '{target_username}' with password 'password123'."))

        with transaction.atomic():
            # 1. Update User Role
            # Get or create profile, then set role
            profile, created = Profile.objects.get_or_create(user=user)
            
            if profile.role != Profile.ROLE_HOTEL_MANAGER:
                profile.role = Profile.ROLE_HOTEL_MANAGER
                profile.save(update_fields=['role'])
                self.stdout.write(self.style.SUCCESS(f"Assigned Hotel Manager role to '{target_username}'."))
            else:
                self.stdout.write(f"User '{target_username}' is already a Hotel Manager.")

            # 2. Link Hotels to User
            # Update all hotels that are not already owned by this user
            hotels_to_update = Hotel.objects.exclude(owner=user)
            hotels_count = hotels_to_update.count()
            
            if hotels_count > 0:
                # Update all matching records directly in the DB
                hotels_to_update.update(owner=user)
                self.stdout.write(self.style.SUCCESS(f"Successfully assigned {hotels_count} hotels to '{target_username}'."))
            else:
                total_hotels = Hotel.objects.count()
                self.stdout.write(f"All {total_hotels} hotels are already owned by '{target_username}'.")
