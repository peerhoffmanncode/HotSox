import uuid
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import (
    GenericAPIView,
)

from django.shortcuts import get_object_or_404
from django.db.models import Q

from app_users.models import Sock, SockLike, UserMatch
from .serializers_users import (
    SockSerializer,
    UserForMatchSerializer,
    SockForMatchSerializer,
    SockForMatchWithIDSerializer,
)

from app_mail.tasks import celery_send_mail
from app_home.pre_prediction_algorithm import PrePredictionAlgorithm


class ApiSwipeNextSock(GenericAPIView):
    """Get next sock view"""

    permission_classes = [IsAuthenticated]
    serializer_class = SockForMatchWithIDSerializer

    def get(self, request, *args, **kwargs):

        current_user = request.user
        # get the sock that the user is currently using to swipe
        try:
            current_sock = Sock.objects.get(user=current_user, pk=kwargs["sock_id"])
        except Sock.DoesNotExist:
            return Response(
                {"error": "this sock was not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # get a next sock to swipe for
        next_sock = PrePredictionAlgorithm.get_next_sock(current_user, current_sock)

        print(current_user, current_sock, Sock.objects.all())

        if next_sock:
            # return the sock as json
            serialize_sock = SockForMatchWithIDSerializer(next_sock)
            return Response(serialize_sock.data, status=status.HTTP_200_OK)
        # no more socks to swipe for
        return Response({"error": "no more socks"}, status=status.HTTP_404_NOT_FOUND)


class ApiJudgeSock(GenericAPIView):
    """Judge a sock view"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_user = request.user
        # get the sock that the user is currently using to swipe
        try:
            current_user_sock = Sock.objects.get(
                user=current_user, pk=kwargs["sock_id"]
            )
        except Sock.DoesNotExist:
            return Response(
                {"error": "your sock was not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            sock_to_be_decided_on = Sock.objects.get(pk=kwargs["other_sock_id"])
        except Sock.DoesNotExist:
            return Response(
                {"error": "sock to decide on was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if current_user_sock.user == sock_to_be_decided_on.user:
            return Response(
                {"error": "You can not like your own sock!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.query_params.get("like", None):
            return Response(
                {
                    "error": "You need to set the like query parameter to either true or false"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Store the decision in the database
        if request.query_params.get("like") == "true":

            # we use get_or_create to beware of duplicates!
            sock_instance, sock_like_created = SockLike.objects.get_or_create(
                sock=current_user_sock, like=sock_to_be_decided_on
            )
            if not sock_like_created:
                # return a message of now new match
                return Response(
                    {
                        "message": f"sock <{sock_to_be_decided_on.pk}> was already liked",
                        "match": "no new match",
                    },
                    status=status.HTTP_208_ALREADY_REPORTED,
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
                    match_message = "Please visit HotSox to check your new match :)"
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

                    # return a message of a new match
                    match_json = {
                        "user": UserForMatchSerializer(current_user_sock.user).data,
                        "other_user": UserForMatchSerializer(
                            sock_to_be_decided_on.user
                        ).data,
                        "sock": SockForMatchSerializer(current_user_sock).data,
                        "other_sock": SockForMatchSerializer(
                            sock_to_be_decided_on
                        ).data,
                        "chatroom_uuid": user_match_object.chatroom_uuid,
                    }

                    return Response(
                        {
                            "message": f"sock <{sock_to_be_decided_on.pk}> was liked",
                            "match": match_json,
                        },
                        status=status.HTTP_201_CREATED,
                    )

            # return a message of now new match
            return Response(
                {
                    "message": f"sock <{sock_to_be_decided_on.pk}> was liked",
                    "match": "no new match",
                },
                status=status.HTTP_201_CREATED,
            )

        # return 201 created, sock was disliked!
        return Response(
            {"message": f"sock <{sock_to_be_decided_on.pk}> was disliked"},
            status=status.HTTP_201_CREATED,
        )
