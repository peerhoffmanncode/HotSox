from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
)

from django.shortcuts import get_object_or_404

from app_users.models import MessageMail
from .serializers_users import (
    MailSerializer,
)

from app_geo.utilities import GeoLocation
from app_mail.tasks import celery_send_mail


# create custom permission handling for methods
class IsAuthenticatedOrAllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


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
