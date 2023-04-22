from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from app_users.models import User, Sock


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
        self.sock1 = Sock.objects.create(
            user=self.user1,
            info_joining_date=date.today() - timedelta(days=365 * 5),
            info_name="Fuzzy Wuzzy",
            info_about="Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
            info_color="5",
            info_fabric="2",
            info_fabric_thickness="7",
            info_brand="13",
            info_type="4",
            info_size="7",
            info_age=10,
            info_separation_date=date.today() - timedelta(days=365),
            info_condition="9",
            info_holes=3,
            info_kilometers=1000,
            info_inoutdoor="1",
            info_washed=2,
            info_special="Once won first place in a sock puppet competition",
        )
        self.sock2 = Sock.objects.create(
            user=self.user2,
            info_joining_date=date.today() - timedelta(days=365 * 5),
            info_name="Fuzzy Wuzzy",
            info_about="Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
            info_color="5",
            info_fabric="2",
            info_fabric_thickness="7",
            info_brand="13",
            info_type="4",
            info_size="7",
            info_age=10,
            info_separation_date=date.today() - timedelta(days=365),
            info_condition="9",
            info_holes=3,
            info_kilometers=1000,
            info_inoutdoor="1",
            info_washed=2,
            info_special="Once won first place in a sock puppet competition",
        )

    @mock.patch("cloudinary.uploader.upload")
    def test_user_upload_profilepic(self, mock_uploader_upload):
        username = TEST_USER2["username"]
        password = TEST_USER2["password"]

        # set up the mock return value
        mock_uploader_upload = "https://cloudinary.com/mock_image.jpg"

        # send a request to add a profile picture
        picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )
        response = self.client.post(
            reverse(
                "app_restapi:api_sock_profilepic_create", kwargs={"pk": self.sock2.pk}
            ),
            data={"profile_picture": picture},
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the response is what we expect
        assert response.status_code == 201

        # check that the user in the database has the new profile picture
        try:
            db_sock = Sock.objects.get(user=self.user2, pk=self.sock2.pk)
        except Sock.DoesNotExist:
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
        response = self.client.post(
            reverse(
                "app_restapi:api_sock_profilepic_create", kwargs={"pk": self.sock2.pk}
            ),
            data={"profile_picture": picture},
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the response is what we expect
        assert response.status_code == 201

        response = self.client.delete(
            reverse(
                "app_restapi:api_sock_profilepic_delete",
                kwargs={"pk": self.sock2.pk, "pk": 1},
            ),
            headers=token(self.client, username="testuser2", password="testuser2"),
        )

        # check that the user in the database has the new profile picture
        try:
            db_sock = Sock.objects.get(user=self.user2, pk=self.sock2.pk)
        except Sock.DoesNotExist:
            db_sock = None
        assert db_sock
        assert len(db_sock.get_all_pictures()) == 0
