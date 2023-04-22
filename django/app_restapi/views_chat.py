from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
)

from django.shortcuts import get_object_or_404

from app_users.models import User, MessageChat
from .serializers_users import (
    ChatSerializer,
    ChatSendSerializer,
)

from app_geo.utilities import GeoLocation
from app_mail.tasks import celery_send_mail


# create custom permission handling for methods
class IsAuthenticatedOrAllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class ApiGetChats(ListAPIView):
    """List of all Chats"""

    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        queryset = MessageChat.objects.all().filter(user=user).order_by("-pk")
        # serialize user instance
        serialized_user = ChatSerializer(queryset, many=True).data
        return Response(data=serialized_user, status=status.HTTP_200_OK)


class ApiGetSendChat(GenericAPIView):
    """
    Get a chat with a specific receiver
    Sned a chat to a specific receiver
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ChatSendSerializer
        return ChatSerializer

    def get(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        receiver_user = get_object_or_404(User, username=kwargs.get("receiver", None))

        if user and receiver_user and user != receiver_user:
            queryset = (
                MessageChat.objects.all()
                .filter(user=user, other=receiver_user)
                .order_by("-pk")
            )
            # serialize user instance
            serialized_user = ChatSerializer(queryset, many=True).data
            return Response(data=serialized_user, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # we do not send chats via websockets here
    # i could be done, but for now (MVP) we just "send" chats via storing data in the database!
    def post(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        receiver_user = get_object_or_404(User, username=kwargs.get("receiver", None))

        if user and receiver_user and user != receiver_user:
            chat = MessageChat.objects.create(
                user=user, other=receiver_user, **request.data
            )

            # serialize instance
            serialized_chat = ChatSerializer(chat).data
            return Response(data=serialized_chat, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
