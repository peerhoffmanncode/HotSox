from django.test import TestCase

from datetime import date
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from .models import User, UserProfilePicture, Sock, SockProfilePicture


# Create your tests here.
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

    def test_user_str(self):
        # Check that the __str__ method returns the expected string
        self.assertEqual(str(self.user1), "<User Quirk Unicorn -> [quirk-unicorn]>")

    def test_is_18_years_method(self):
        # Check that the is_18_years method returns True for users over 18 years old
        self.assertTrue(self.user1.is_18_years())
        # Create a test user who is 17 years old
        # Check that the is_18_years method returns False for users under 18 years old
        self.assertFalse(self.user2.is_18_years())

    def test_to_json_method(self):
        # Check that the to_json method returns a dictionary with the expected keys and values
        expected_json = {
            "username": "quirk-unicorn",
            "fullname": "Quirk Unicorn",
            "email": "quirk-unicorn@example.com",
            "about": "I like to collect rubber ducks",
            "age": 23,
            "city": "Rainbow City",
            "instagram": "https://www.instagram.com/quirk_unicorn/",
            "facebook": "https://www.facebook.com/quirk_unicorn/",
            "twitter": "https://www.twitter.com/quirk_unicorn/",
            "spotify": "https://www.spotify.com/quirk_unicorn/",
        }
        self.assertEqual(self.user1.to_json(), expected_json)

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

    def test_user_get_age(self):
        self.assertEqual(self.user1.get_age(), 23)

    def test_user_delete(self):
        # create a profile picture and a sock for the user
        user_profile_picture = UserProfilePicture.objects.create(
            user=self.user1, profile_picture=None
        )

        sock_profile_picture = SockProfilePicture.objects.create(
            sock=self.sock, profile_picture=None
        )
        # delete the user
        self.user1.delete()

        # check that the profile picture are deleted
        self.assertFalse(
            get_user_model().objects.filter(username="quirk-unicorn").exists()
        )

        # check that the socks are deleted
        self.assertFalse(
            UserProfilePicture.objects.filter(pk=user_profile_picture.pk).exists()
        )
        # check that the socks are deleted
        self.assertFalse(Sock.objects.filter(pk=self.sock.pk).exists())
        self.assertFalse(
            SockProfilePicture.objects.filter(pk=sock_profile_picture.pk).exists()
        )

    def test_sock_deletion(self):
        # create a sock profile picture to test deletion
        sock_profile_picture = SockProfilePicture.objects.create(
            sock=self.sock, profile_picture=None
        )
        # delete the sock
        self.sock.delete()
        # check sock is gone
        self.assertEqual(Sock.objects.count(), 0)
        # check sock profile picture is gone
        self.assertEqual(SockProfilePicture.objects.count(), 0)

    def test_sock_string_representation(self):
        self.assertEqual(str(self.sock), "<Sock Test Sock>")
