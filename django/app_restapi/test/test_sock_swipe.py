from unittest import mock
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_users.models import User, Sock, SockProfilePicture, MessageMail, MessageChat

from datetime import date, timedelta

from .inital_test_setup import (
    TEST_USER1,
    TEST_USER2,
    token,
)

from rest_framework.test import APIClient

sock_data1 = {
    "info_name": "Main Sock",
    "info_about": "This is a new fake sock.",
    "info_color": 1,
    "info_fabric": 1,
    "info_fabric_thickness": 1,
    "info_brand": 1,
    "info_type": 1,
    "info_size": 1,
    "info_age": 1,
    "info_separation_date": str(date.today() + timedelta(days=1)),
    "info_condition": 1,
    "info_holes": 1,
    "info_kilometers": 1,
    "info_inoutdoor": 1,
    "info_washed": 1,
    "info_special": "main sock!",
}
sock_data2 = {
    "info_name": "Test Sock1",
    "info_about": "This is a new fake sock.",
    "info_color": 1,
    "info_fabric": 1,
    "info_fabric_thickness": 1,
    "info_brand": 1,
    "info_type": 1,
    "info_size": 1,
    "info_age": 1,
    "info_separation_date": str(date.today() + timedelta(days=1)),
    "info_condition": 1,
    "info_holes": 1,
    "info_kilometers": 1,
    "info_inoutdoor": 1,
    "info_washed": 1,
    "info_special": "Test sock!",
}


class TestUser(TestCase):
    @mock.patch("cloudinary.uploader.upload")
    def setUp(self, mocky_the_mockmock):
        mock_uploader_upload = "https://cloudinary.com/mock_image.jpg"

        self.client = APIClient()
        self.user1 = User.objects.create_superuser(**TEST_USER1)
        self.user2 = User.objects.create_user(**TEST_USER2)
        self.sock1 = Sock.objects.create(user=self.user1, **sock_data1)
        self.sock2 = Sock.objects.create(user=self.user2, **sock_data2)

        # send a request to add a profile picture
        picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )
        token(self.client, username="admin", password="admin")
        response = self.client.post(
            reverse(
                "app_restapi:api_sock_profilepic_create",
                kwargs={"sock_id": self.sock1.pk},
            ),
            data={"profile_picture": picture},
        )

        # send a request to add a profile picture
        picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )
        token(self.client, username="testuser2", password="testuser2")
        response = self.client.post(
            reverse(
                "app_restapi:api_sock_profilepic_create",
                kwargs={"sock_id": self.sock2.pk},
            ),
            data={"profile_picture": picture},
        )

    def test_swipe_next_sock(self):

        token(self.client, "admin", "admin")
        response = self.client.get(
            reverse("app_restapi:api_next_sock", kwargs={"sock_id": self.sock1.pk}),
            format="json",
        )
        content = response.json()

        assert response.status_code == 200
        assert content["id"] == self.sock2.pk

    def test_swipe_next_sock_invalide(self):

        token(self.client, "admin", "admin")
        response = self.client.get(
            reverse("app_restapi:api_next_sock", kwargs={"sock_id": 2}),
            format="json",
        )
        content = response.json()

        assert response.status_code == 400
        assert content == {"error": "this sock was not found"}

    @mock.patch("app_restapi.views_swipe.celery_send_mail")
    def test_swipe_judge_sock(self, mock):
        mock.return_value = "mocked"

        token(self.client, "admin", "admin")

        # judge first sock
        response = self.client.post(
            reverse(
                "app_restapi:api_judge_sock",
                kwargs={
                    "sock_id": self.sock1.pk,
                    "other_sock_id": self.sock2.pk,
                },
            )
            + "?like=true",
            format="json",
        )
        content = response.json()
        assert response.status_code == 201
        assert content == {
            "message": f"sock <{self.sock2.pk}> was liked",
            "match": "no new match",
        }

        # judge first sock again
        response = self.client.post(
            reverse(
                "app_restapi:api_judge_sock",
                kwargs={
                    "sock_id": self.sock1.pk,
                    "other_sock_id": self.sock2.pk,
                },
            )
            + "?like=true",
            format="json",
        )
        content = response.json()
        assert response.status_code == 208
        assert content == {
            "message": f"sock <{self.sock2.pk}> was already liked",
            "match": "no new match",
        }

        token(self.client, "testuser2", "testuser2")
        # other user judge first sock to get match!
        response = self.client.post(
            reverse(
                "app_restapi:api_judge_sock",
                kwargs={
                    "sock_id": self.sock2.pk,
                    "other_sock_id": self.sock1.pk,
                },
            )
            + "?like=true",
            format="json",
        )
        content = response.json()
        assert response.status_code == 201
        assert content.get("match")
        assert content["match"]["user"]["username"] == self.user2.username
        assert content["match"]["other_user"]["username"] == self.user1.username
        assert len(content["match"]["chatroom_uuid"]) == 36
