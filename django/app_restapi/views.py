from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
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
    ChatSendSerializer,
    MailSerializer,
    SockSerializer,
)

from app_geo.utilities import GeoLocation
from app_mail.tasks import celery_send_mail


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

    # serializer_class = UserCreateSerializer
    # generate different serializer classes for different methods
    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        elif self.request.method == "PUT":
            return UserUpdateSerializer
        return UserSerializer

    def get(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        # serialize user instance
        serialized_user = UserSerializer(user).data
        return Response(data=serialized_user, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                data=UserSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # get expected user instance
        serializer = UserUpdateSerializer(instance=request.user, data=request.data)
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


class ApiGetMails(ListCreateAPIView):
    """List of all Mails"""

    permission_classes = [IsAuthenticated]
    queryset = MessageMail.objects.all().order_by("-pk")
    serializer_class = MailSerializer

    def get(self, request, *args, **kwargs):
        # get expected user instance
        queryset = MessageMail.objects.all().filter(user=request.user).order_by("-pk")
        # serialize user instance
        serialized_mail = MailSerializer(queryset, many=True).data
        return Response(data=serialized_mail, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user
        serializer = MailSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save(user=request.user)
            # send actual mail via celery
            celery_send_mail.delay(
                email_subject=result.subject,
                email_message=result.content,
                recipient_list=[result.user.email],
                notification=result.user.notification,
            )
            return Response(
                data=MailSerializer(result).data, status=status.HTTP_201_CREATED
            )


class ApiDeleteMail(DestroyAPIView):
    """Destroy mail view"""

    permission_classes = [IsAuthenticated]

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


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

    def post(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        receiver_user = get_object_or_404(User, username=kwargs.get("receiver", None))

        if user and receiver_user and user != receiver_user:
            print(request.data)
            chat = MessageChat.objects.create(
                user=user, other=receiver_user, **request.data
            )

            # serialize instance
            serialized_chat = ChatSerializer(chat).data
            return Response(data=serialized_chat, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
