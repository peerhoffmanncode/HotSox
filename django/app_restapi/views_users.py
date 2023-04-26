from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from django.shortcuts import get_object_or_404

from app_users.models import User, UserProfilePicture
from .serializers_users import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserProfilePicSerializer,
)


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
    """Get, create, update or delete a user"""
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


class ApiCreateProfilePic(CreateAPIView):
    """Create a new profile picture"""
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    # queryset = UserProfilePicture.objects.all()
    serializer_class = UserProfilePicSerializer

    def post(self, request):
        serializer = UserProfilePicSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save(user=request.user)
            return Response(
                data=UserProfilePicSerializer(result).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDeleteProfilePic(GenericAPIView):
    """Delete a profile picture"""
    permission_classes = [IsAuthenticated]

    queryset = UserProfilePicture.objects.all()
    serializer_class = UserProfilePicSerializer

    def delete(self, request, *args, **kwargs):
        try:
            picture = UserProfilePicture.objects.get(user=request.user, pk=kwargs["pk"])
        except UserProfilePicture.DoesNotExist:
            return Response(
                {"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        if picture:
            picture.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
