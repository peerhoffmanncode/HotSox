from unittest import mock
from django.test import TestCase
from django.urls import reverse
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

    def test_show_users_login_incorrect_cedentials(self):
        response = self.client.get(reverse("app_restapi:api_user_list"), format="json")
        assert response.status_code == 401

    def test_show_users_login_incorrect_permission(self):
        response = self.client.get(
            reverse("app_restapi:api_user_list"),
            headers=token(self.client, "testuser2", "testuser2"),
            format="json",
        )
        assert response.status_code == 403

    def test_show_users_login_correct_cedentials(self):
        response = self.client.get(
            reverse("app_restapi:api_user_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        content = response.json()["results"]
        assert response.status_code == 200
        assert len(content) == 2
        assert content[0].get("username") == "testuser2"
        assert content[1].get("username") == "admin"

    def test_show_user_admin(self):
        response = self.client.get(
            reverse("app_restapi:api_user_crud"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 200
        # check for correct user

        db_user = User.objects.get(username="admin")
        assert db_user
        for key in TEST_USER1.keys():
            if key != "password":
                assert key in db_user.__dict__.keys()

    def test_show_user_that_do_not_exist(self):
        response = self.client.get(
            reverse("app_restapi:api_user_crud"),
            headers=token(self.client, "DoNotExist", "DoNotExist"),
            format="json",
        )
        assert response.status_code == 401
        # test database if user really do not exist

        try:
            db_user = User.objects.filter(username="DoNotExist")
        except User.DoesNotExist:
            db_user = None
        assert not db_user

    def test_update_user_admin(self):
        update_data = {
            "username": "admin",
            "first_name": "UPDATED1",
            "last_name": "UPDATED2",
            "email": "admin@admin.com",
            "info_about": "admin",
            "info_birthday": "1001-01-01",
            "info_gender": "1",
            "location_city": "AdminCity",
            "location_latitude": 0,
            "location_longitude": 0,
            "notification": True,
            "social_instagram": "",
            "social_facebook": "",
            "social_twitter": "",
            "social_spotify": "",
        }

        response = self.client.put(
            reverse("app_restapi:api_user_crud"),
            data=update_data,
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 202
        assert response.json()["username"] == update_data["username"]
        assert response.json()["first_name"] == update_data["first_name"]
        assert response.json()["last_name"] == update_data["last_name"]
        assert response.json()["social_instagram"] == update_data["social_instagram"]
        assert response.json()["social_spotify"] == update_data["social_spotify"]
        # check that the user is updated in the database
        db_user = User.objects.get(username="admin")
        assert db_user.username == update_data["username"]
        assert db_user.first_name == update_data["first_name"]
        assert db_user.last_name == update_data["last_name"]
        assert db_user.social_instagram == update_data["social_instagram"]
        assert db_user.social_spotify == update_data["social_spotify"]

    def test_update_user_that_do_not_exist(self):
        update_data = {
            "username": "admin",
            "first_name": "UPDATED1",
            "last_name": "UPDATED2",
            "email": "admin@admin.com",
            "info_about": "admin",
            "info_birthday": "1001-01-01",
            "info_gender": 1,
            "location_city": "AdminCity",
            "location_latitude": 0,
            "location_longitude": 0,
            "notification": True,
            "social_instagram": "UPDATE4",
            "social_facebook": "",
            "social_twitter": "",
            "social_spotify": "UPDATE3",
        }

        response = self.client.put(
            reverse("app_restapi:api_user_crud") + "DoNotExist",
            data=update_data,
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 404
        # check that the user do not exist in the database
        try:
            db_user = User.objects.get(username="DoNotExist")
        except User.DoesNotExist:
            db_user = None
        assert db_user == None

    def test_create_user_wrong_data(self):
        create_data = {
            "username": "bibo",
            "first_name": "bibo",
            "last_name": "bibo",
            "email": "bibo@bibo.com",
            "info_about": "bibo",
            "info_birthday": "2001-01-01",
            "info_gender": 4,
            "location_city": "biboCity",
            "location_latitude": 50,
            "location_longitude": 8,
            "notification": True,
            "social_instagram": "",
            "social_facebook": "",
            "social_twitter": "",
            "social_spotify": "",
        }

        response = self.client.post(
            reverse("app_restapi:api_user_crud"),
            data=create_data,
            headers=token(self.client, "admin", "admin"),
        )
        assert response.status_code == 400
        assert response.json()["password"] == ["This field is required."]
        # check if element exists in the database
        try:
            db_user = User.objects.get(username=create_data["username"])
        except User.DoesNotExist:
            db_user = None
        assert db_user == None

    def test_create_user_new(self):
        create_data = {
            "username": "bibo",
            "first_name": "bibo",
            "last_name": "bibo",
            "email": "bibo@bibo.com",
            "info_about": "bibo",
            "info_birthday": "2001-01-01",
            "info_gender": "4",
            "location_city": "Mainz",
            "location_latitude": 50.0012314,
            "location_longitude": 8.2762513,
            "notification": True,
            "social_instagram": "",
            "social_facebook": "",
            "social_twitter": "",
            "social_spotify": "",
            "password": "bibobibo",
        }

        response = self.client.post(
            reverse("app_restapi:api_user_crud"),
            data=create_data,
            format="json",
        )

        assert response.status_code == 201
        for key, value in create_data.items():
            if key != "password":
                assert response.json()[key] == value

        # check if element exists in the database
        try:
            db_user = User.objects.get(username=create_data["username"])
        except User.DoesNotExist:
            db_user = None
        assert db_user

    def test_create_user_dupliceate(self):
        create_data = {
            "username": "bibo",
            "first_name": "bibo",
            "last_name": "bibo",
            "email": "bibo@bibo.com",
            "info_about": "bibo",
            "info_birthday": "2001-01-01",
            "info_gender": 4,
            "location_city": "biboCity",
            "location_latitude": 50,
            "location_longitude": 8,
            "notification": True,
            "social_instagram": "",
            "social_facebook": "",
            "social_twitter": "",
            "social_spotify": "",
            "password": "bibobibo",
        }
        # create new user
        response = self.client.post(
            reverse("app_restapi:api_user_crud"),
            data=create_data,
            format="json",
        )
        assert response.status_code == 201

        db_user = User.objects.get(username=create_data["username"])
        assert db_user

        # check for duplicate username
        response = self.client.post(
            reverse("app_restapi:api_user_crud"),
            data=create_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "username": ["A user with that username already exists."],
            "email": ["user with this email address already exists."],
        }

    # @mock.patch("api.database.models.destroy_profilepicture_on_cloud")
    def test_delete_user(self):
        # mock_celery.return_value = {"message": f"user profile picture was deleted"}

        response = self.client.delete(
            reverse("app_restapi:api_user_crud"),
            headers=token(self.client, "admin", "admin"),
        )
        assert response.status_code == 204
        # check if element done not exists in the database

        try:
            db_user = User.objects.get(username="admin")
        except User.DoesNotExist:
            db_user = None
        assert db_user == None

    # @mock.patch("api.database.models.destroy_profilepicture_on_cloud")
    def test_delete_noneexisting_user(self):
        # mock_celery.return_value = {"message": f"user profile picture was deleted"}

        response = self.client.delete(
            reverse("app_restapi:api_user_crud"),
            headers=token(self.client, "DoNotExist", "DoNotExist"),
            format="json",
        )
        assert response.status_code == 401
