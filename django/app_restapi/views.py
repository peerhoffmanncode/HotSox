from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    # RetrieveUpdateDestroyAPIView,
)

from app_users.models import User, MessageMail, MessageChat, Sock
from .serializers_users import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChatSerializer,
    MailSerializer,
    SockSerializer,
)


class ApiGetUsers(ListAPIView):
    """List of all Users"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiCreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        result = super().post(request, *args, **kwargs)
        print(result)
        print(dir(result))


class ApiGetUser(RetrieveAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiUpdateUser(UpdateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


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
