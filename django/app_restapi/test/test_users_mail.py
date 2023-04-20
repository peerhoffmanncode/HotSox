from unittest import mock
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse

from app_users.models import User, MessageMail


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

    def test_user_mails_no_mails_in_db(self):
        response = self.client.get(
            reverse("app_restapi:api_mail_list"),
            headers=token(self.client, "admin", "admin"),
            format="json",
        )
        assert response.status_code == 200
        assert response.json()["results"] == []

    # @mock.patch("api.controller.ctr_mail.celery_send_mail_to_user")
    # def test_user_mail_send(mock_send_message, self):
    #     # setup mock
    #     mock_send_message.return_value = {
    #         "subject": "TestMailSubject",
    #         "content": "TestMailContent",
    #     }

    #     response = self.client.post(
    #         reverse("app_restapi:api_mail_send"),
    #         headers=token(self.client, "admin", "admin"),
    #         data={
    #             "subject": "TestMailSubject",
    #             "content": "TestMailContent",
    #         },
    #         format="json",
    #     )
    #     assert response.status_code == 200
    #     assert response.json() == {
    #         "status": "email has been sent",
    #         "email": {
    #             "subject": "TestMailSubject",
    #             "content": "TestMailContent",
    #         },
    #     }

    #     # double check database feedback
    #     response = self.client.get(
    #         reverse("app_restapi:api_mail_list"),
    #         headers=token(self.client, "admin", "admin"),
    #         format="json",
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["results"][0]["content"] == "TestMailContent"
    #     assert response.json()["results"][0]["subject"] == "TestMailSubject"

    # @mock.patch("api.controller.ctr_mail.celery_send_mail_to_user")
    # def test_user_mail_delete(mock_send_message, self):
    #     # setup db

    #     # get user
    #     user = User.objects.get(username="admin")
    #     # create mail
    #     mail = MessageMail.objects.create(
    #         user=user, subject="TestMailSubject", content="TestMailContent"
    #     )

    #     # delete mail
    #     response = self.client.delete(
    #         reverse("app_restapi:api_mail_delete", kwargs={"pk": mail.pk}),
    #         headers=token(self.client, "admin", "admin"),
    #         format="json",
    #     )

    #     # get all remaining mails after delete
    #     try:
    #         mail = MessageMail.objects.get(pk=mail.pk)
    #     except MessageMail.DoesNotExist:
    #         mail = None

    #     assert response.status_code == 204
    #     assert not mail
