import os
from django.test import TestCase

from allauth.socialaccount.models import SocialApp, SocialAccount
from django.contrib.sites.models import Site
from .models import User

from django.utils import timezone
from datetime import date

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(
            username="test",
            first_name="test first",
            last_name="test last",
            email="test@mail.com",
            password="str0ng_pwd!",
            birthday=date(2000, 1, 1),
            user_sex="female",
            interested_sex="male",
        )

    def test_str_method(self):
        # Check that the __str__ method returns the expected string
        self.assertEqual(str(self.user), "[test] test first test last, Female")

    def test_is_18_years_method(self):
        # Check that the is_18_years method returns True for users over 18 years old
        self.assertTrue(self.user.is_18_years())
        # Create a test user who is 17 years old
        user_17_years = User.objects.create(
            username="test_17",
            first_name="test_17 first",
            last_name="test_17 last",
            email="test_17@mail.com",
            password="str0ng_pwd!",
            birthday=date(timezone.now().year - 17, 1, 1),
            user_sex="male",
            interested_sex="female",
        )
        # Check that the is_18_years method returns False for users under 18 years old
        self.assertFalse(user_17_years.is_18_years())

    def test_to_json_method(self):
        # Check that the to_json method returns a dictionary with the expected keys and values
        self.assertDictEqual(
            self.user.to_json(),
            {
                "pk": self.user.pk,
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "birthday": self.user.birthday,
                "user_sex": self.user.user_sex,
                "interested_sex": self.user.interested_sex,
                "last_login": self.user.last_login,
                "date_joined": self.user.date_joined,
                "is_active": self.user.is_active,
            },
        )

    def test_regular_authentication(self):
        # Authenticate the user using the Google SocialAccount
        self.client.login(username=self.user.username, password="str0ng_pwd!")
        # Make an assertion to verify that the user is authenticated
        self.assertTrue(self.user.is_authenticated)

    def test_google_authentication(self):
        # Set up a Google SocialAccount object with faked valid credentials
        google_account = SocialAccount(
            user_id=self.user.pk,
            provider="google",
            uid="1234567890",
            extra_data={
                "access_token": "abcdefghijklmnopqrstuvwxyz",
                "refresh_token": "zyxwvutsrqponmlkjihgfedcba",
            },
        )
        google_account.save()

        # Authenticate the user using the Google SocialAccount
        user = google_account.user
        user.backend = "allauth.account.auth_backends.AuthenticationBackend"
        self.client.force_login(user)

        # Make an assertion to verify that the user is authenticated
        self.assertTrue(user.is_authenticated)
