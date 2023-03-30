from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from app_users.models import User, MessageMail, MessageChat, Sock
from .serializers_users import (
    UserSerializer,
    ChatSerializer,
    MailSerializer,
    SockSerializer,
)


class ApiGetUsers(ListAPIView):
    """List of all Users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiGetUser(RetrieveAPIView):
    """Detail view of the User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ApiGetMails(ListAPIView):
    """List of all Mails"""

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetMail(RetrieveAPIView):
    """Detail mail view"""

    queryset = MessageMail.objects.all()
    serializer_class = MailSerializer


class ApiGetChats(ListAPIView):
    """List of all Chats"""

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetChat(RetrieveAPIView):
    """List of all Chats"""

    queryset = MessageChat.objects.all()
    serializer_class = ChatSerializer


class ApiGetSocks(ListAPIView):
    """Lists all socks"""

    queryset = Sock.objects.all()
    serializer_class = SockSerializer


class ApiGetSock(RetrieveAPIView):
    """Sock detail view"""

    queryset = Sock.objects.all()
    serializer_class = SockSerializer
