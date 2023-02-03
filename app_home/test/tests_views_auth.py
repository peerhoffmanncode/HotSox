from django.test import TestCase
from app_users.models import User
from datetime import date


class Test(TestCase):
    def test_about_view_none_restricted(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_home/about.html")

    def test_restricted_area_index(self):
        # create test user
        user = User.objects.create(
            username="test",
            first_name="test first",
            last_name="test last",
            email="test@mail.com",
            password="str0ng_pwd!",
            info_birthday=date(2000, 1, 1),
            info_about="I like to collect rubber ducks",
            info_gender="male",
            location_city="Rainbow City",
            location_latitude=0,
            location_longitude=0,
            social_instagram="https://www.instagram.com/quirk_unicorn/",
            social_facebook="https://www.facebook.com/quirk_unicorn/",
            social_twitter="https://www.twitter.com/quirk_unicorn/",
            social_spotify="https://www.spotify.com/quirk_unicorn/",
        )
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.content, b"<h1>Please first log in to access this")

    def test_restricted_area_index_login(self):
        # create test user
        user = User.objects.create(
            username="test",
            first_name="test first",
            last_name="test last",
            email="test@mail.com",
            password="str0ng_pwd!",
            info_birthday=date(2000, 1, 1),
            info_about="I like to collect rubber ducks",
            info_gender="male",
            location_city="Rainbow City",
            location_latitude=0,
            location_longitude=0,
            social_instagram="https://www.instagram.com/quirk_unicorn/",
            social_facebook="https://www.facebook.com/quirk_unicorn/",
            social_twitter="https://www.twitter.com/quirk_unicorn/",
            social_spotify="https://www.spotify.com/quirk_unicorn/",
        )
        self.client.force_login(user=user)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"<h1>Well done, you see the Hot Sox HomePage !</h1>", response.content
        )

    def test_restricted_area_index_login_missing_user_details(self):
        # create test user
        user = User.objects.create(
            username="test",
            first_name="test first",
            last_name="test last",
            email="test@mail.com",
            password="str0ng_pwd!",
            info_birthday=date(2000, 1, 1),
            info_about="I like to collect rubber ducks",
            info_gender="",  # missing !
            location_city="",  # missing !
            location_latitude=0,
            location_longitude=0,
            social_instagram="",
            social_facebook="",
            social_twitter="",
            social_spotify="",
        )
        self.client.force_login(user=user)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.content, b"<h1>Please first log in to access this")
