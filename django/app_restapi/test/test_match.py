import uuid
from unittest import mock

from app_users.models import User, UserMatch
from rest_framework.test import APIClient

from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase
from django.urls import reverse

from .inital_test_setup import TEST_USER1, TEST_USER2, token


class TestUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_superuser(**TEST_USER1)
        self.user2 = User.objects.create_user(**TEST_USER2)
        self.match1 = UserMatch.objects.create(
            user=self.user1,
            other=self.user2,
            unmatched=False,
            chatroom_uuid=uuid.uuid4(),
        )

    def test_all_matches(self):
        # login
        token(self.client, username="admin", password="admin")

        # call api
        response = self.client.get(
            reverse("app_restapi:api_match_list"),
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]["id"] == self.match1.pk
        assert response.json()[0]["unmatched"] == False
        assert len(response.json()[0]["chatroom_uuid"]) == 36
        assert response.json()[0]["user"] == self.user1.pk
        assert response.json()[0]["other"] == self.user2.pk

    def test_specific_match(self):
        # login first user
        token(self.client, username="admin", password="admin")

        # call api
        response = self.client.get(
            reverse(
                "app_restapi:api_match_specific",
                kwargs={"pk": self.match1.pk},
            ),
        )
        print(response.json())
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["id"] == self.match1.pk
        assert response.json()["user"] == self.user1.pk
        assert response.json()["other"] == self.user2.pk
        assert response.json()["unmatched"] == False
        assert len(response.json()["chatroom_uuid"]) == 36

        # login second user
        token(self.client, username="testuser2", password="testuser2")

        # call api
        response = self.client.get(
            reverse(
                "app_restapi:api_match_specific",
                kwargs={"pk": self.match1.pk},
            ),
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        assert response.json()["id"] == self.match1.pk
        assert response.json()["user"] == self.user2.pk
        assert response.json()["other"] == self.user1.pk
        assert response.json()["unmatched"] == False
        assert len(response.json()["chatroom_uuid"]) == 36

    @mock.patch("app_restapi.views_match.celery_send_mail")
    def test_delete_match_user1_perspective(self, mock_celery_send_mail):
        mock_celery_send_mail.return_value = "mocked"
        # check from first user perspective

        # login second user
        token(self.client, username="admin", password="admin")

        # call api
        response = self.client.delete(
            reverse(
                "app_restapi:api_match_delete",
                kwargs={"pk": self.match1.pk},
            ),
        )

        # get match obejct from database
        match_object = UserMatch.objects.get(pk=self.match1.pk)

        assert response.status_code == 200
        assert response.json()["message"] == "successfully unmatched"
        assert match_object.unmatched == True

    @mock.patch("app_restapi.views_match.celery_send_mail")
    def test_delete_match_user2_perspective(self, mock_celery_send_mail):
        mock_celery_send_mail.return_value = "mocked"
        # check from first user perspective

        # login second user
        token(self.client, username="testuser2", password="testuser2")

        # call api
        response = self.client.delete(
            reverse(
                "app_restapi:api_match_delete",
                kwargs={"pk": self.match1.pk},
            ),
        )

        # get match obejct from database
        match_object = UserMatch.objects.get(pk=self.match1.pk)

        assert response.status_code == 200
        assert response.json()["message"] == "successfully unmatched"
        assert match_object.unmatched == True
