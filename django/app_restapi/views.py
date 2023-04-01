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

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiCreateUser(GenericAPIView):

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(User, username=serializer.data.get("username"))
            # geodata injection
            try:
                (
                    user.location_latitude,
                    user.location_longitude,
                ) = GeoLocation.get_geolocation_from_city(user.location_city)
            except:
                user.location_latitude = 0
                user.location_longitude = 0
            # update user
            user.save()
            return Response(
                data=serializer.validated_data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiGetPutDeleteUser(GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
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
            serializer.save()
            # geodata injection
            try:
                (
                    user.location_latitude,
                    user.location_longitude,
                ) = GeoLocation.get_geolocation_from_city(user.location_city)
            except:
                user.location_latitude = 0
                user.location_longitude = 0
            # update user
            user.save()
            return Response(
                data=serializer.validated_data, status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiGetMails(ListAPIView):
    """List of all Mails"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetMail(RetrieveAPIView):
    """Detail mail view"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetChats(ListAPIView):
    """List of all Chats"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetChat(RetrieveAPIView):
    """List of all Chats"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetSocks(ListAPIView):
    """Lists all socks"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Sock.objects.all()
    serializer_class = SockSerializer


class ApiGetSock(RetrieveAPIView):
    """Sock detail view"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Sock.objects.all()
    serializer_class = SockSerializer
