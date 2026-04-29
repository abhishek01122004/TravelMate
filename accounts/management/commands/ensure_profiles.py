from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "Create a Profile for any User that is missing one (default role: traveler)."

    def handle(self, *args, **options):
        created_count = 0
        for user in User.objects.all().iterator():
            _, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": Profile.ROLE_TRAVELER},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Profile created for {user.username}"))
        if created_count == 0:
            self.stdout.write("All users already have a profile.")
        else:
            self.stdout.write(self.style.SUCCESS(f"Done. Created {created_count} profile(s)."))
