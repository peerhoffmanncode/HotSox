from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView

from django.shortcuts import get_object_or_404

from app_users.models import UserMatch, User
from .serializers_users import MatchSerializer

from app_mail.tasks import celery_send_mail


class ApiGetAllMatches(ListAPIView):
    """View to retrieve all matches for one user"""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        matches = UserMatch.objects.filter(Q(user=user) | Q(other=user))
        if matches:
            return Response(
                data=MatchSerializer(matches, many=True).data, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "No matches found :("}, status=status.HTTP_404_NOT_FOUND
        )


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
