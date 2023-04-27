from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_users.models import User, Sock

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
    def setUp(self):

        self.client = APIClient()
        self.user1 = User.objects.create_superuser(**TEST_USER1)
        self.user2 = User.objects.create_user(**TEST_USER2)
        self.sock1 = Sock.objects.create(user=self.user1, **sock_data1)
        self.sock2 = Sock.objects.create(user=self.user2, **sock_data2)

    @mock.patch("cloudinary.uploader.upload")
    def test_sock_upload_profilepic(self, mock_uploader_upload):
        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload = "https://cloudinary.com/mock_image.jpg"

        db_user = User.objects.get(username=username)

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

        # check that the response is what we expect
        assert response.status_code == 201

        # check that the user in the database has the new profile picture
        try:
            db_sock = Sock.objects.get(pk=self.sock2.pk)
        except User.DoesNotExist:
            db_sock = None
        assert db_sock
        assert len(db_sock.get_all_pictures()) == 1

    @mock.patch("app_users.models.destroy_profilepicture_on_cloud")
    @mock.patch("cloudinary.uploader.upload")
    def test_user_delete_profilepic(self, mock_uploader_upload, mock_destroy):
        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload = True
        mock_destroy = True

        # make a test user
        db_user = User.objects.get(username=username)

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

        # check that the response is what we expect
        assert response.status_code == 201
        try:
            db_sock = Sock.objects.get(pk=self.sock2.pk)
        except Sock.DoesNotExist:
            db_sock = None
        assert db_sock
        assert len(db_sock.get_all_pictures()) == 1
        picture_id = response.json()["id"]

        token(self.client, username="testuser2", password="testuser2")
        response = self.client.delete(
            reverse(
                "app_restapi:api_sock_profilepic_delete",
                kwargs={"sock_id": self.sock2.pk, "pic_id": picture_id},
            ),
        )

        # check that the user in the database has the new profile picture
        try:
            db_sock = Sock.objects.get(pk=self.sock2.pk)
        except Sock.DoesNotExist:
            db_sock = None
        assert db_sock
        assert len(db_sock.get_all_pictures()) == 0
