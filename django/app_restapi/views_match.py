from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from django.shortcuts import get_object_or_404

from app_users.models import UserMatch, User, MessageChat, MessageMail
from .serializers_users import MatchSerializer

from app_mail.tasks import celery_send_mail


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
    """Doc here"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass


class ApiDeleteSpecificMatch(GenericAPIView):
    """View to delete a specific Match"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        
        # get current user
        current_user = request.user
        match = UserMatch.objects.filter(Q(user=current_user) | Q(other=current_user)).filter(pk=kwargs.get("pk"))

        if not match:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        # get all the chat messages between the users
        chat_messages = MessageChat.objects.filter(
            Q(user=match.user, other=match.other)
            | Q(user=match.other, other=match.user)
        )
        # delete the chat messages
        for message in chat_messages:
            message.delete()

        # set all the match objects to unmatched = True
        match.unmatched = True
        match.save()

        if match.user == current_user:
            match_user = match.other
        else:
            match_user = match.user
    
        # email to confirm deleted match
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
        return Response(status=status.HTTP_204_NO_CONTENT)

