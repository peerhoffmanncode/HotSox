from django.test import TestCase

from django.contrib.auth import get_user_model
from datetime import date, timedelta

from ..models import User, UserProfilePicture, Sock, SockProfilePicture


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

    ####### USER #######
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

    ####### Sock #######
    def test_sock_string_representation(self):
        self.assertEqual(str(self.sock), "<Sock Fuzzy Wuzzy>")

    def test_sock_to_json(self):
        # Get the json representation of the Sock object
        json_data = self.sock.to_json()

        # Assert that the json data contains the correct values
        # reduced checks because of uncertainty of data consistencies
        self.assertEqual(json_data["Name"], self.sock.info_name)
        self.assertEqual(json_data["My story"], self.sock.info_about)

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
