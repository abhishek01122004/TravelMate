from accounts.models import Profile


def hotel_manager_nav(request):
    is_hotel_manager = False
    if request.user.is_authenticated:
        try:
            is_hotel_manager = request.user.profile.role == Profile.ROLE_HOTEL_MANAGER
        except Profile.DoesNotExist:
            pass
    return {"is_hotel_manager": is_hotel_manager}
