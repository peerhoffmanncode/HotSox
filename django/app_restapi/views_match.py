from app_mail.tasks import celery_send_mail
from app_users.models import MessageChat, MessageMail, User, UserMatch
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404

from .serializers_users import MatchSerializer


class ApiGetAllMatches(ListAPIView):
    """View to retrieve all matches for one user"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        matches = UserMatch.objects.filter(Q(user=user) | Q(other=user))
        if matches:
            return Response(
                data=MatchSerializer(matches, many=True).data, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "No matches found :("}, status=status.HTTP_404_NOT_FOUND
        )


class ApiGetSpecificMatch(GenericAPIView):
    """View to show a specific match"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # logged in user is user in the UserMatch object
        try:
            current_match = UserMatch.objects.get(
                user=user, pk=kwargs.get("pk")
            )
            serialized_match = MatchSerializer(current_match).data
            return Response(data=serialized_match, status=status.HTTP_200_OK)
        except UserMatch.DoesNotExist:
            # logged in user is other in the UserMatch object
            try:
                current_match = UserMatch.objects.get(
                    other=user, pk=kwargs.get("pk")
                )
                serialized_match = MatchSerializer(current_match).data
                # switch user and other in the serialized data
                # so that the logged in user is always the user
                serialized_match["user"], serialized_match["other"] = serialized_match["other"], serialized_match["user"]
                return Response(data=serialized_match, status=status.HTTP_200_OK)
            except UserMatch.DoesNotExist:
                return Response(
                    {"Message": "Match could not be found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

class ApiDeleteSpecificMatch(GenericAPIView):
    """View to unmatch a specific match"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        # get current user
        current_user = request.user
        match = UserMatch.objects.filter(
            Q(user=current_user) | Q(other=current_user)
        ).filter(pk=kwargs.get("pk")).first()

        if not match:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # get all the chat messages between the users and delete them
        chat_messages = MessageChat.objects.filter(
            Q(user=match.user, other=match.other)
            | Q(user=match.other, other=match.user)
        ).delete()

        # set all the match objects to unmatched = True
        match.unmatched = True
        match.save()

        if match.user == current_user:
            match_user = match.other
        else:
            match_user = match.user

        # email to confirm unmatch a match
        match_message = f"The match between {match_user.username} and {current_user.username} has been deleted"
        celery_send_mail.delay(
            email_subject=f"You have unmached with {match_user.username}",
            email_message=match_message,
            recipient_list=[current_user.email],
            notification=current_user.notification,
        )
        celery_send_mail.delay(
            email_subject=f"{current_user.username} has unmached you",
            email_message=match_message,
            recipient_list=[match_user.email],
            notification=match_user.notification,
        )

        # return to match overview
        return Response({"message": "successfully unmatched"}, status=status.HTTP_200_OK)
