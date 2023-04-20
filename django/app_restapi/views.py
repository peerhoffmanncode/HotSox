from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from django.shortcuts import get_object_or_404

from app_users.models import User, MessageMail, MessageChat, Sock
from .serializers_users import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChatSerializer,
    MailSerializer,
    SockSerializer,
)

from app_geo.utilities import GeoLocation
from rest_framework import permissions


# create custom permission handling for methods
class IsAuthenticatedOrAllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class ApiGetUsers(ListAPIView):
    """List of all Users"""

    permission_classes = [IsAdminUser]

    queryset = User.objects.all().order_by("-pk")
    serializer_class = UserSerializer


class ApiGetPutCreateDeleteUser(GenericAPIView):
    permissions.SAFE_METHODS = ["POST"]
    permission_classes = [IsAuthenticatedOrAllowAny]
    serializer_class = UserUpdateSerializer

    # show user with id
    def get(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        # serialize user instance
        serialized_user = UserSerializer(user).data
        return Response(data=serialized_user, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(
                data=UserSerializer(updated_user).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                data=UserSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiGetMails(ListAPIView):
    """List of all Mails"""

    permission_classes = [IsAdminUser]

    queryset = MessageMail.objects.all().order_by("-pk")
    serializer_class = MailSerializer


class ApiGetMail(RetrieveAPIView):
    """Detail mail view"""

    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetChats(ListAPIView):
    """List of all Chats"""

    permission_classes = [IsAdminUser]

    queryset = MessageChat.objects.all().order_by("-pk")
    serializer_class = ChatSerializer


class ApiGetChat(RetrieveAPIView):
    """List of all Chats"""

    permission_classes = [IsAuthenticated]

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetSocks(ListAPIView):
    """Lists all socks"""

    permission_classes = [IsAdminUser]

    queryset = Sock.objects.all().order_by("-pk")
    serializer_class = SockSerializer


class ApiGetSock(RetrieveAPIView):
    """Sock detail view"""

    permission_classes = [IsAuthenticated]

    queryset = Sock.objects.all()
    serializer_class = SockSerializer
