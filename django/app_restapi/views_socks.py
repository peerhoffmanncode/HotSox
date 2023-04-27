from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)

from django.shortcuts import get_object_or_404

from app_users.models import Sock, SockProfilePicture
from .serializers_users import (
    SockSerializer,
    SockCreateSerializer,
    SockUpdateSerializer,
    SockProfilePictureSerializer,
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
    serializer_class = SockSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Sock.objects.filter(user=current_user).order_by("-pk")


class ApiCreateSock(GenericAPIView):
    """Create a sock"""

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
    """Get, update or delete a sock"""

    permission_classes = [IsAuthenticated]

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


class ApiCreateSockProfilePic(CreateAPIView):
    """Create a new profile picture"""

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    # queryset = UserProfilePicture.objects.all()
    serializer_class = SockProfilePictureSerializer

    def post(self, request, *args, **kwargs):
        current_user = request.user
        try:
            current_sock = Sock.objects.get(user=current_user, pk=kwargs.get("sock_id"))
            picture_serializer = SockProfilePictureSerializer(data=request.data)
            if picture_serializer.is_valid():
                result = picture_serializer.save(sock=current_sock)
                return Response(
                    data=SockProfilePictureSerializer(result).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                picture_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Sock.DoesNotExist:
            return Response(
                {"error": "Could not find sock"}, status=status.HTTP_400_BAD_REQUEST
            )


class ApiDeleteSockProfilePic(GenericAPIView):
    """Delete a profile picture"""

    permission_classes = [IsAuthenticated]

    queryset = SockProfilePicture.objects.all()
    serializer_class = SockProfilePictureSerializer

    def delete(self, request, *args, **kwargs):
        current_user = request.user
        try:
            current_sock = Sock.objects.get(user=current_user, pk=kwargs.get("sock_id"))
        except Sock.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            picture = SockProfilePicture.objects.get(
                sock=current_sock, pk=kwargs["pic_id"]
            )
        except SockProfilePicture.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        if picture:
            picture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
