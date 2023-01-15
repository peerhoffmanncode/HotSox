from django.test import TestCase
from app_users.models import User
from datetime import date


class Test(TestCase):
    def test_home_view_none_restricted(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_home/index.html")

    def test_restricted_area_prove_of_concept_no_access(self):
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
        response = self.client.get("/prove-of-concept/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'<h1>Please first log in to access this page.</h1><br><a href="/user/login">Sign in</a>',
        )

    def test_restricted_area_prove_of_concept_access(self):
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
        response = self.client.get("/prove-of-concept/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'<h1>Seems like you are logged in! Yeay! </h1><p>Nice job Test!</p><br><a href="/">return to home</a>',
        )
