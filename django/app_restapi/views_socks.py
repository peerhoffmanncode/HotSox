from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from django.shortcuts import get_object_or_404

from app_users.models import Sock
from .serializers_users import (
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
