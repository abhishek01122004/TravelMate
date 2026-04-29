from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance, raw, **kwargs):
    """
    Every user gets a Profile (traveler by default).
    Uses get_or_create so older users created before this app still get a row
    the next time their User is saved (e.g. from Django admin).
    """
    if raw:
        return
    Profile.objects.get_or_create(
        user=instance,
        defaults={"role": Profile.ROLE_TRAVELER},
    )

