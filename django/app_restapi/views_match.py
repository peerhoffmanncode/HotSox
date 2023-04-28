from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from django.shortcuts import get_object_or_404

from app_users.models import UserMatch, User
from .serializers_users import MatchSerializer

from app_mail.tasks import celery_send_mail


class ApiGetAllMatches(GenericAPIView):
    """Doc here"""

    """maybe a list view?"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass


class ApiGetSpecificMatch(GenericAPIView):
    """Doc here"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pass


class ApiDeleteSpecificMatch(GenericAPIView):
    """Doc here"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pass
