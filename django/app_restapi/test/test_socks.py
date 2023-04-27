from unittest import mock
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from app_users.models import User, Sock

from datetime import datetime, date, timedelta

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

    def test_show_all_socks_of_a_user_no_socks(self):
        response = self.client.get(
            reverse("app_restapi:api_sock_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        content = response.json()

        assert content == {"count": 0, "next": None, "previous": None, "results": []}

    def test_show_all_socks_of_a_user_with_socks(self):
        db_user = User.objects.get(username="admin")
        sock1 = Sock.objects.create(
            user=db_user,
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

        sock2 = Sock.objects.create(
            user=db_user,
            info_joining_date=datetime.utcnow(),
            info_name="Sock2",
            info_about="This is a fake sock2.",
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

        # check socks for current user (with socks!)
        response = self.client.get(
            reverse("app_restapi:api_sock_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        content = response.json()["results"]
        assert response.status_code == 200
        assert len(content) == 2

        # check socks for other user (with no socks!)
        response = self.client.get(
            reverse("app_restapi:api_sock_list"),
            headers=token(self.client, "testuser2", "testuser2"),
            format="json",
        )
        content = response.json()
        assert content == {"count": 0, "next": None, "previous": None, "results": []}

    def test_show_sock_of_a_user_no_sock(self):
        response = self.client.get(
            reverse("app_restapi:api_sock_rud", kwargs={"pk": 1}),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 400
        assert response.data == None

    def test_show_sock_of_a_user_with_sock(self):
        db_user = User.objects.get(username="admin")
        sock1 = Sock.objects.create(
            user=db_user,
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

        response = self.client.get(
            reverse("app_restapi:api_sock_rud", kwargs={"pk": sock1.pk}),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        content = response.json()
        assert response.status_code == 200
        assert isinstance(content, dict)
        assert content["info_about"] == "This is a fake sock."
        assert content["info_age"] == 7
        assert content["info_brand"] == "4"
        assert content["info_color"] == "1"
        assert content["info_condition"] == "8"
        assert content["info_fabric"] == "2"
        assert content["info_fabric_thickness"] == "3"
        assert content["info_holes"] == 9
        assert content["info_inoutdoor"] == "9"
        assert content["info_kilometers"] == 10
        assert content["info_name"] == "Sock1"
        assert content["info_size"] == "6"
        assert content["info_special"] == "None"
        assert content["info_type"] == "5"
        assert content["info_washed"] == 12
        assert content["profile_picture"] == []
        assert content["sock_likes"] == []

    def test_update_sock_of_a_user_with_sock(self):
        db_user = User.objects.get(username="admin")
        sock1 = Sock.objects.create(
            user=db_user,
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

        update_data = {
            "info_name": "_update_Sock1",
            "info_about": "This is a updated fake sock.",
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
            "info_special": "Update",
        }
        response = self.client.put(
            reverse("app_restapi:api_sock_rud", kwargs={"pk": sock1.pk}),
            headers=token(self.client, "admin", "admin"),
            data=update_data,
            format="json",
        )
        content = response.json()
        assert response.status_code == 202
        assert isinstance(content, dict)
        assert content["info_about"] == "This is a updated fake sock."
        assert content["info_age"] == 1
        assert content["info_brand"] == "1"
        assert content["info_color"] == "1"
        assert content["info_condition"] == "1"
        assert content["info_fabric"] == "1"
        assert content["info_fabric_thickness"] == "1"
        assert content["info_holes"] == 1
        assert content["info_inoutdoor"] == "1"
        assert content["info_kilometers"] == 1
        assert content["info_name"] == "_update_Sock1"
        assert content["info_separation_date"] == str(date.today() + timedelta(days=1))
        assert content["info_size"] == "1"
        assert content["info_special"] == "Update"
        assert content["info_type"] == "1"
        assert content["info_washed"] == 1

    def test_create_and_delete_sock_of_a_user(self):
        db_user = User.objects.get(username="admin")
        all_socks_before = Sock.objects.filter(user=db_user)
        len(all_socks_before)  # odd bug - without this line the test fails!!
        sock_data = {
            "info_name": "new_Sock3",
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
            "info_special": "NEW!",
        }

        # create sock
        response = self.client.post(
            reverse("app_restapi:api_sock_create"),
            headers=token(self.client, "admin", "admin"),
            data=sock_data,
            format="json",
        )
        # validate sock
        content = response.json()
        assert response.status_code == 201
        assert isinstance(content, dict)
        assert content["info_about"] == "This is a new fake sock."
        assert content["info_age"] == 1
        assert content["info_brand"] == "1"
        assert content["info_color"] == "1"
        assert content["info_condition"] == "1"
        assert content["info_fabric"] == "1"
        assert content["info_fabric_thickness"] == "1"
        assert content["info_holes"] == 1
        assert content["info_inoutdoor"] == "1"
        assert content["info_kilometers"] == 1
        assert content["info_name"] == "new_Sock3"
        assert content["info_separation_date"] == str(date.today() + timedelta(days=1))
        assert content["info_size"] == "1"
        assert content["info_special"] == "NEW!"
        assert content["info_type"] == "1"
        assert content["info_washed"] == 1

        # delete sock
        db_user = User.objects.get(username="admin")
        all_socks_after = Sock.objects.filter(user=db_user)

        # check one more sock in the database for correct user
        assert len(all_socks_after) == len(all_socks_before) + 1

        response = self.client.delete(
            reverse("app_restapi:api_sock_rud", kwargs={"pk": all_socks_after[0].pk}),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        db_user = User.objects.get(username="admin")
        all_socks_after = Sock.objects.filter(user=db_user)
        # check one more sock in the database for correct user

        assert response.status_code == 204
        # check that created sock is deleted
        assert len(all_socks_after) == len(all_socks_before)
        assert len(all_socks_after) == 0
