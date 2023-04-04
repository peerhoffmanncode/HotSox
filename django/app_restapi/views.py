from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
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


class ApiGetUsers(ListAPIView):
    """List of all Users"""

    permission_classes = [IsAuthenticated]

    queryset = User.objects.all().order_by("-pk")
    serializer_class = UserSerializer


class ApiCreateUser(GenericAPIView):

    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                data=UserSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiGetPutDeleteUser(GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    # show user with id
    def get(self, request, *args, **kwargs):
        # get expected user instance
        user = get_object_or_404(User, pk=kwargs["pk"])
        # serialize user instance
        serialized_user = UserSerializer(user).data
        return Response(data=serialized_user, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # get expected user instance
        user = get_object_or_404(User, pk=kwargs["pk"])

        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(
                data=UserSerializer(updated_user).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiGetMails(ListAPIView):
    """List of all Mails"""

    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all().order_by("-pk")
    serializer_class = MailSerializer


class ApiGetMail(RetrieveAPIView):
    """Detail mail view"""

    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetChats(ListAPIView):
    """List of all Chats"""

    permission_classes = [IsAuthenticated]

    queryset = MessageChat.objects.all().order_by("-pk")
    serializer_class = ChatSerializer


class ApiGetChat(RetrieveAPIView):
    """List of all Chats"""

    permission_classes = [IsAuthenticated]

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetSocks(ListAPIView):
    """Lists all socks"""

    permission_classes = [IsAuthenticated]

    queryset = Sock.objects.all().order_by("-pk")
    serializer_class = SockSerializer


class ApiGetSock(RetrieveAPIView):
    """Sock detail view"""

    permission_classes = [IsAuthenticated]

    queryset = Sock.objects.all()
    serializer_class = SockSerializer
