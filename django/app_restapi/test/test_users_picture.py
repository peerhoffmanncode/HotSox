from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_users.models import User


from .inital_test_setup import (
    TEST_USER1,
    TEST_USER2,
    token,
)

from rest_framework.test import APIClient


class TestUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_superuser(**TEST_USER1)
        self.user2 = User.objects.create_user(**TEST_USER2)

    @mock.patch("cloudinary.uploader.upload")
    def test_user_upload_profilepic(self, mock_uploader_upload):
        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload = "https://cloudinary.com/mock_image.jpg"

        db_user = User.objects.get(username=username)

        # send a request to add a profile picture
        picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )
        response = self.client.post(
            reverse("app_restapi:api_user_profilepic_create"),
            data={"profile_picture": picture},
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the response is what we expect
        assert response.status_code == 201

        # check that the user in the database has the new profile picture
        try:
            db_user = User.objects.get(username=username)
        except User.DoesNotExist:
            db_user = None
        assert db_user
        assert len(db_user.get_all_pictures()) == 1

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
        response = self.client.post(
            reverse("app_restapi:api_user_profilepic_create"),
            data={"profile_picture": picture},
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the response is what we expect
        assert response.status_code == 201

        response = self.client.delete(
            reverse("app_restapi:api_user_profilepic_delete", kwargs={"pk": 1}),
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the user in the database has the new profile picture
        try:
            db_user = User.objects.get(username=username)
        except User.DoesNotExist:
            db_user = None
        assert db_user
        assert len(db_user.get_all_pictures()) == 0
