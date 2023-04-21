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

    def test_user_chats_no_chats(self):
        response = self.client.get(
            reverse("app_restapi:api_chats_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.json() == []

    def test_user_chats_with_chats(self):

        user1 = User.objects.get(username=TEST_USER1["username"])
        user2 = User.objects.get(username=TEST_USER2["username"])
        MessageChat.objects.create(user=user1, other=user2, message="test message")

        response = self.client.get(
            reverse("app_restapi:api_chats_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 200
        assert response.json()[0]["other"] == {
            "username": "testuser2",
            "email": "testuser2@testuser2.com",
        }
        assert response.json()[0]["message"] == "test message"
        assert response.json()[0]["seen_date"] == None

    def test_user_chats_no_chats_between_users(self):
        response = self.client.get(
            reverse(
                "app_restapi:api_chat_get_send",
                kwargs={"receiver": TEST_USER2["username"]},
            ),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.json() == []

    def test_user_chats_with_chats_between_users(self):

        user1 = User.objects.get(username=TEST_USER1["username"])
        user2 = User.objects.get(username=TEST_USER2["username"])
        MessageChat.objects.create(user=user1, other=user2, message="test message")

        response = self.client.get(
            reverse(
                "app_restapi:api_chat_get_send",
                kwargs={"receiver": TEST_USER2["username"]},
            ),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 200
        response_json = response.json()[0]
        assert response_json["other"] == {
            "username": "testuser2",
            "email": "testuser2@testuser2.com",
        }
        assert response_json["message"] == "test message"
        assert response_json["seen_date"] == None
