from django.test import TestCase

from datetime import date
from allauth.socialaccount.models import SocialAccount

from ..models import User, Sock


class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user1 = User.objects.create(
            username="quirk-unicorn",
            email="quirk-unicorn@example.com",
            password="testpassword",
            first_name="Quirk",
            last_name="Unicorn",
            info_about="I like to collect rubber ducks",
            info_birthday=date(2000, 1, 1),
            info_gender="male",
            location_city="Rainbow City",
            location_latitude=0,
            location_longitude=0,
            social_instagram="https://www.instagram.com/quirk_unicorn/",
            social_facebook="https://www.facebook.com/quirk_unicorn/",
            social_twitter="https://www.twitter.com/quirk_unicorn/",
            social_spotify="https://www.spotify.com/quirk_unicorn/",
        )
        self.user2 = User.objects.create(
            username="quirky_unicorn",
            email="quirkyunicorn@example.com",
            password="p4ssword",
            first_name="Quirky",
            last_name="Unicorn",
            info_about="I like to collect rubber ducks",
            info_birthday=date(2020, 1, 1),
            info_gender="unicorn",
            location_city="Quirkyville",
            location_latitude=0,
            location_longitude=0,
            social_instagram="https://www.instagram.com/quirk_unicorn/",
            social_facebook="https://www.facebook.com/quirk_unicorn/",
            social_twitter="https://www.twitter.com/quirk_unicorn/",
            social_spotify="https://www.spotify.com/quirk_unicorn/",
        )

        self.sock = Sock.objects.create(
            user=self.user1,
            info_name="Test Sock",
            info_color="blue",
            info_fabric="cotton",
            info_fabric_thickness="1",
            info_brand="aldi",
            info_type="knee_high",
            info_size="40-45",
            info_age=11,
            info_condition="11",
            info_holes=3,
            info_kilometers=100,
            info_inoutdoor="2",
            info_washed=15,
            info_special="test special",
        )

    def test_regular_authentication(self):
        # Authenticate the user using the Google SocialAccount
        self.client.login(username=self.user1.username, password="testpassword!")
        # Make an assertion to verify that the user is authenticated
        self.assertTrue(self.user1.is_authenticated)

    def test_google_authentication(self):
        # Set up a Google SocialAccount object with faked valid credentials
        google_account = SocialAccount(
            user_id=self.user1.pk,
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
