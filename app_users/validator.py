from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Sock


def user_validate_hotsox_information(request):
    """Utility function to validate a user setting!
    If user details are missing, redirect to profile page again!
    """
    current_user = get_object_or_404(User, pk=request.user.pk)

    if (
        not current_user.is_18_years()
        or not current_user.info_gender
        or not current_user.location_city
    ):
        return False
    return True


class HotSoxLogInAndValidationCheckMixin(LoginRequiredMixin):
    """Extension to the regular LoginRequiredMixin
    to include the HotSox validation!"""

    def dispatch(self, request, *args, **kwargs):
        """Django's build in validation function.
        We included our own validation process to check
        if all necessary user details are given.
        If something crucial is missing,
        we redirect to user-profile-update
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if user_validate_hotsox_information(request):
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse("app_users:user-profile-update"))


class ProtectedSockMixin(LoginRequiredMixin):
    """Extension to the regular LoginRequiredMixin
    to include the HotSox validation!"""

    def dispatch(self, request, *args, **kwargs):
        try:
            sock = Sock.objects.get(pk=kwargs["pk"])
            if sock.user == request.user:
                return super().dispatch(request, *args, **kwargs)
            return redirect(reverse("app_home:index"))
        except Sock.DoesNotExist:
            return redirect(reverse("app_home:index"))
