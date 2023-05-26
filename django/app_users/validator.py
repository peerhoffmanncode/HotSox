from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Sock, User


def prompt_user_msg(request, msg) -> None:
    """Function to send a message to the user. Only if it is not already displayed"""
    for message in messages.get_messages(request):
        if msg.strip() == str(message).strip():
            # do not send msg
            return
    # send msg
    messages.warning(request, msg)


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
        # flush session
        if request.session.get("sock_pk"):
            request.session.pop("sock_pk")
        if request.session.get("redirect_url"):
            request.session.pop("redirect_url")

        # prompt user for action
        prompt_user_msg(request, "Please ensure your profile is fully completed and accurate")

        # return not valid!
        return False

    # if user has no profile picture uploaded, advise him to upload a picture
    if not current_user.get_all_pictures():
        # prompt user for action
        prompt_user_msg(request, "Please upload at least one picture to your user profile")

    # if user has no sock added, advise him to add a sock
    if not current_user.get_socks():
        # prompt user for action
        prompt_user_msg(request, "Please add a sock to your profile")

    # return valid!
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
            sock = Sock.objects.get(pk=request.session["sock_pk"])
            if sock.user == request.user:
                return super().dispatch(request, *args, **kwargs)
            # user has no ownership of the sock, redirect to home!
            request.session["sock_pk"] = None
            return redirect(reverse("app_home:index"))
        except Sock.DoesNotExist:
            # cant't find the sock in db, redirect to overview
            request.session["sock_pk"] = None
            return redirect(reverse("app_users:sock-overview"))
        except KeyError:
            # cant't find the sock in current session. redirect to overview
            request.session["sock_pk"] = None
            return redirect(reverse("app_users:sock-overview"))
