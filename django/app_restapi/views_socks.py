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
    SockCreateSerializer,
    SockUpdateSerializer,
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

    permission_classes = [IsAuthenticated]

    # queryset = Sock.objects.all().order_by("-pk")
    serializer_class = SockSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Sock.objects.filter(user=current_user).order_by("-pk")


class ApiCreateSock(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SockCreateSerializer

    def post(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        serialized_sock = SockCreateSerializer(data=request.data)
        if serialized_sock.is_valid():
            serialized_sock.save(user=user)
            return Response(data=serialized_sock.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ApiGetPutDeleteSock(GenericAPIView):
    permission_classes = [IsAuthenticated]

    # serializer_class = UserCreateSerializer
    # generate different serializer classes for different methods
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return SockUpdateSerializer
        return SockSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            current_sock = Sock.objects.get(user=user, pk=kwargs.get("pk"))
            serialized_sock = SockSerializer(current_sock).data
            return Response(data=serialized_sock, status=status.HTTP_200_OK)
        except Sock.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # get expected user instance
        user = request.user
        try:
            current_sock = Sock.objects.get(user=user, pk=kwargs.get("pk"))
            serialized_sock = SockUpdateSerializer(
                instance=current_sock, data=request.data
            )
            if serialized_sock.is_valid():
                serialized_sock.save()
                return Response(
                    data=serialized_sock.data, status=status.HTTP_202_ACCEPTED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Sock.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        try:
            current_sock = Sock.objects.get(user=user, pk=kwargs.get("pk"))
            current_sock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Sock.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
