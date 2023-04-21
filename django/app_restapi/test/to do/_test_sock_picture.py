from unittest import mock
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from app_users.models import User, MessageMail, MessageChat


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

    @mock.patch("api.controller.ctr_sock_pic.uploader.upload")
    def test_user_upload_profilepic(mock_uploader_upload, test_db_setup):
        with Session(engine) as db:
            username = TEST_USER2["username"]
            password = TEST_USER2["password"]

            # set up the mock return value
            mock_uploader_upload.return_value = {
                "url": "https://cloudinary.com/mock_image.jpg"
            }

            # make a test user
            db_user = db.query(User).filter(User.username == username).first()
            db_user_sock = Sock(
                user_id=db_user.id,
                info_joining_date=datetime.utcnow(),
                info_name="Sock1",
                info_about="This is a fake sock.",
                info_color=1,
                info_fabric=2,
                info_fabric_thickness=3,
                info_brand=4,
                info_type=5,
                info_size=6,
                info_age=7,
                info_separation_date=date.today(),
                info_condition=8,
                info_holes=9,
                info_kilometers=10,
                info_inoutdoor=9,
                info_washed=12,
                info_special="None",
            )

            db.add(db_user_sock)
            db.commit()
            db.refresh(db_user_sock)

            # send a request to add a profile picture
            with open("./requirements.txt", "rb") as mock_file:
                response = client.post(
                    f"{PREFIX}/user/sock/{db_user_sock.id}/profilepic",
                    files={"file": ("filename", mock_file)},
                    headers=token(username="testuser2", password="testuser2"),
                )

            # check that the response is what we expect
            print(response.json())
            assert response.status_code == 201
            assert (
                response.json()["profile_picture"]
                == "https://cloudinary.com/mock_image.jpg"
            )

            # check that the user in the database has the new profile picture
            db_user_sock = db.query(Sock).filter(Sock.id == db_user_sock.id).first()
            assert len(db_user_sock.profile_pictures) == 1
            assert (
                db_user_sock.profile_pictures[0].profile_picture
                == "https://cloudinary.com/mock_image.jpg"
            )

    @mock.patch("api.database.models.destroy_profilepicture_on_cloud")
    @mock.patch("api.database.models.uploader.destroy")
    @mock.patch("api.controller.ctr_sock_pic.uploader.upload")
    def test_user_delete_profilepic(
        mock_uploader_upload,
        mock_uploader_destroy,
        mock_celery,
        test_db_setup,
    ):
        with Session(engine) as db:
            username = TEST_USER2["username"]
            password = TEST_USER2["password"]

            # set up the mock return value
            mock_uploader_upload.return_value = {
                "url": "https://cloudinary.com/mock_image.jpg"
            }
            mock_uploader_destroy.return_value = True
            mock_celery.return_value = {"message": f"user profile picture was deleted"}

            # make a test user
            db_user = db.query(User).filter(User.username == username).first()
            db_user_sock = Sock(
                user_id=db_user.id,
                info_joining_date=datetime.utcnow(),
                info_name="Sock1",
                info_about="This is a fake sock.",
                info_color=1,
                info_fabric=2,
                info_fabric_thickness=3,
                info_brand=4,
                info_type=5,
                info_size=6,
                info_age=7,
                info_separation_date=date.today(),
                info_condition=8,
                info_holes=9,
                info_kilometers=10,
                info_inoutdoor=9,
                info_washed=12,
                info_special="None",
            )

            db.add(db_user_sock)
            db.commit()
            db.refresh(db_user_sock)

            # send a request to add a profile picture
            with open("./requirements.txt", "rb") as mock_file:
                response = client.post(
                    f"{PREFIX}/user/sock/{db_user_sock.id}/profilepic",
                    files={"file": ("filename", mock_file)},
                    headers=token(username="testuser2", password="testuser2"),
                )

            # make a test user and get all pictures
            before_delete_profilepics = db_user_sock.profile_pictures

            # send a request to delete a profile picture
            response = client.request(
                "DELETE",
                f"{PREFIX}/user/sock/{db_user_sock.id}/profilepic/{before_delete_profilepics[0].id}",
                headers=token("testuser2", "testuser2"),
            )

            # check that the response is what is expect
            assert response.status_code == 204

        # new session to persist changes of transactions before!
        with Session(engine) as db:
            # check that the user in the database has the new profile picture
            db_sock_new = db.query(Sock).filter(Sock.id == db_user_sock.id).first()
            assert (
                len(db_sock_new.profile_pictures) == len(before_delete_profilepics) - 1
            )
