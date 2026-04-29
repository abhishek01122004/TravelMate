from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import Profile


def hotel_manager_required(view_func):
    """Allow only users whose Profile.role is hotel_manager."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        try:
            role = request.user.profile.role
        except Profile.DoesNotExist:
            messages.error(request, "Account profile not found.")
            return redirect("home")

        if role != Profile.ROLE_HOTEL_MANAGER:
            messages.error(request, "This page is for hotel managers only.")
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper
