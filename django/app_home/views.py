from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
import uuid

from app_users.validator import HotSoxLogInAndValidationCheckMixin
from app_users.models import User, Sock, SockLike, UserMatch
from .pre_prediction_algorithm import PrePredictionAlgorithm
from app_geo.utilities import GeoLocation

from app_mail.tasks import celery_send_mail


class HomeView(HotSoxLogInAndValidationCheckMixin, TemplateView):
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.username:
            user = User.objects.get(username=request.user.username)
            user.username = user.username.title()
            context = {"user": user}
        else:
            context = {"user": None}

        return render(request, "app_home/index.html", context)

    def post(self, request, *args, **kwargs):
        pass


class AboutView(TemplateView):
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.username:
            user = User.objects.get(username=request.user.username)
            user.username = user.username.title()
            context = {"user": user}
        else:
            context = {"user": None}

        return render(request, "app_home/about.html", context)

    def post(self, request, *args, **kwargs):
        pass


class SwipeView(HotSoxLogInAndValidationCheckMixin, TemplateView):
    model = User
    template_name = "app_home/swipe.html"

    def get(self, request, *args, **kwargs):
        """show initial swipe view with a pre predicted sock"""
        if request.session.get("sock_pk", None):
            # get a pre predicted sock
            sock = PrePredictionAlgorithm.get_next_sock(
                current_user=request.user,
                current_user_sock=get_object_or_404(
                    Sock, pk=request.session["sock_pk"]
                ),
            )
            # get all socks related to the current user (queryset)
            user_socks = Sock.objects.filter(user=request.user)
            if sock:
                context = {
                    "sock": sock.serialize_attributes(),
                    "user_socks": user_socks,
                }
            else:
                context = {"sock": None, "user_socks": user_socks}
            return render(request, "app_home/swipe.html", context)
        # fail back route
        return redirect(reverse("app_users:sock-overview"))

    def post(self, request, *args, **kwargs):
        """function to either like or dislike a sock
        can also change the selected sock of the user"""

        current_user_sock = get_object_or_404(Sock, pk=request.session["sock_pk"])

        # check if the frontend wants to change the selected user sock
        if request.POST.get("change_sock", None):
            request.session["sock_pk"] = request.POST.get("change_sock", None)
            current_user_sock = get_object_or_404(Sock, pk=request.session["sock_pk"])
            messages.success(
                request,
                f"successfully selected sock {current_user_sock.info_name}.",
            )
            return redirect(reverse("app_home:swipe"))

        sock_to_be_decided_on = get_object_or_404(
            Sock, pk=request.POST.get("sock_pk", None)
        )

        # frontend liked the sock
        if request.POST.get("decision", None) == "like":
            # we use get_or_create to beware of duplicates!
            _, sock_like_created = SockLike.objects.get_or_create(
                sock=current_user_sock, like=sock_to_be_decided_on
            )

            # check for user to user match via the socks
            if current_user_sock in sock_to_be_decided_on.get_likes():
                # create match in UserMatchTable if not already exists!
                try:
                    user_match_object = UserMatch.objects.get(
                        Q(user=current_user_sock.user, other=sock_to_be_decided_on.user)
                        | Q(
                            other=current_user_sock.user,
                            user=sock_to_be_decided_on.user,
                        )
                    )
                    user_match_created = False
                except UserMatch.DoesNotExist:
                    user_match_object = UserMatch.objects.create(
                        user=current_user_sock.user,
                        other=sock_to_be_decided_on.user,
                        chatroom_uuid=uuid.uuid4(),
                    )
                    user_match_created = True

                if user_match_created:
                    # sending match email
                    match_message = "Please visit HotSox to check your new match:)"
                    celery_send_mail.delay(
                        email_subject=f"You have a match with {sock_to_be_decided_on.user.username}",
                        email_message=match_message,
                        recipient_list=[current_user_sock.user.email],
                        notification=current_user_sock.user.notification,
                    )
                    celery_send_mail.delay(
                        email_subject=f"You have a match with {current_user_sock.user.username}",
                        email_message=match_message,
                        recipient_list=[sock_to_be_decided_on.user.email],
                        notification=sock_to_be_decided_on.user.notification,
                    )

                    context = {
                        "user": current_user_sock.user,
                        "user_sock": current_user_sock,
                        "matched_user": sock_to_be_decided_on.user,
                        "distance": GeoLocation.get_distance(
                            (
                                current_user_sock.user.location_latitude,
                                current_user_sock.user.location_longitude,
                            ),
                            (
                                sock_to_be_decided_on.user.location_latitude,
                                sock_to_be_decided_on.user.location_longitude,
                            ),
                        ),
                        "matched_user_sock": sock_to_be_decided_on,
                    }
                    # add navigation arrows
                    context["left_arrow_go_to_url"] = reverse("app_home:swipe")
                    context["right_arrow_go_to_url"] = reverse(
                        "app_users:user-match-profile-details",
                        kwargs={"username": sock_to_be_decided_on.user.username},
                    )

                    return render(request, "app_home/match.html", context)

        # frontend disliked the sock
        elif request.POST.get("decision", None) == "dislike":
            # we use get_or_create to beware of duplicates!
            _, sock_dislike_created = SockLike.objects.get_or_create(
                sock=current_user_sock, dislike=sock_to_be_decided_on
            )

        # reload the frontend
        return redirect(reverse("app_home:swipe"))
