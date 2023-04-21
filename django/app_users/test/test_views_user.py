from django.test import TestCase, Client
from unittest import mock

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from ..models import User, Sock, UserMatch

import uuid


class UserSignUpTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="quirk-unicorn",
            password="!passw@rd123",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
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

        self.sock = Sock.objects.create(
            user=self.user,
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

        self.client = Client()
        self.url = None

    def test_user_signup(self):
        # define URL
        self.url = reverse("app_users:user-signup")

        # Test POST request with valid form data
        response = self.client.post(
            self.url,
            data={
                "username": "123quirk-unicorn",
                "password1": "!passw@rd123",
                "password2": "!passw@rd123",
                "email": "123john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "info_about": "I like to collect rubber ducks",
                "info_birthday": date(2000, 1, 1),
                "info_gender": "2",
                "location_city": "Rainbow City",
                "location_latitude": 0,
                "location_longitude": 0,
                "social_instagram": "https://www.instagram.com/quirk_unicorn/",
                "social_facebook": "https://www.facebook.com/quirk_unicorn/",
                "social_twitter": "https://www.twitter.com/quirk_unicorn/",
                "social_spotify": "https://www.spotify.com/quirk_unicorn/",
            },
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code
        self.assertEqual(
            response["location"], reverse("app_users:user-profile-picture")
        )  # check redirect url
        self.assertEqual(
            User.objects.count(), 2
        )  # check if user is created in the database
        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )  # check if user is logged in

        # Test GET request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # check status code
        # self.assertTemplateUsed(response, "users/signup.html")  # check template

    def test_user_profile_details(self):
        # define URL
        self.url = reverse("app_users:user-profile-details")

        self.client.force_login(self.user)  # logging in user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # check status code
        self.assertTemplateUsed(
            response, "users/profile_details.html"
        )  # check template
        self.assertEqual(
            response.context["left_arrow_go_to_url"], ""
        )  # check left arrow url
        self.assertEqual(
            response.context["right_arrow_go_to_url"],
            reverse("app_users:user-profile-update"),
        )  # check right arrow url

    def test_user_profile_update(self):
        # define URL
        self.url = reverse("app_users:user-profile-update")

        self.client.force_login(self.user)  # logging in user

        # alter the profile data!
        response = self.client.post(
            self.url,
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com",
                "username": "123quirk-unicorn",
                "password1": "!passw@rd123",
                "password2": "!passw@rd123",
                "info_about": "I like to collect rubber ducks",
                "info_birthday": date(2000, 1, 1),
                "info_gender": "2",
                "location_city": "Rainbow City",
                "location_latitude": 0,
                "location_longitude": 0,
                "social_instagram": "https://www.instagram.com/quirk_unicorn/",
                "social_facebook": "https://www.facebook.com/quirk_unicorn/",
                "social_twitter": "https://www.twitter.com/quirk_unicorn/",
                "social_spotify": "https://www.spotify.com/quirk_unicorn/",
            },
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code
        self.assertEqual(
            response.url, reverse("app_users:user-profile-details")
        )  # check redirect url
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.first_name, "Jane")  # check if first_name is updated
        self.assertEqual(
            user.email, "jane.doe@example.com"
        )  # check if email is updated
        self.assertTrue(
            response.wsgi_request.user.is_authenticated
        )  # check if user is logged in

        # Test GET request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # check status code
        self.assertTemplateUsed(response, "users/profile_update.html")  # check template
        self.assertEqual(
            response.context["left_arrow_go_to_url"],
            reverse("app_users:user-profile-details"),
        )  # check left arrow url
        self.assertEqual(
            response.context["right_arrow_go_to_url"],
            reverse("app_users:sock-overview"),
        )  # check right arrow url

    @mock.patch("cloudinary.uploader.upload")
    def test_user_profile_picture_update(self, mock_uploader_upload):
        # mocking
        mock_uploader_upload = "picture.jpg"

        # define URL & image
        self.url = reverse("app_users:user-profile-picture")
        self.picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )

        self.client.force_login(self.user)  # logging in user
        # Test POST request with add method
        response = self.client.post(
            self.url,
            data={
                "method": "add",
                "profile_picture": self.picture,
            },
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code
        self.assertEqual(
            response.url, reverse("app_users:user-profile-picture")
        )  # check redirect url
        self.assertEqual(
            len(self.user.get_all_pictures()), 1
        )  # check if picture is added to the user

        # Test POST request with delete method
        picture_pk = self.user.get_all_pictures()[0].pk
        response = self.client.post(
            self.url,
            data={
                "method": "delete",
                "picture_pk": picture_pk,
            },
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code
        self.assertEqual(
            response.url, reverse("app_users:user-profile-picture")
        )  # check redirect url
        self.assertEqual(
            len(self.user.get_all_pictures()), 0
        )  # check if picture is deleted from the user

        # Test GET request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # check status code
        self.assertTemplateUsed(
            response, "users/profile_picture.html"
        )  # check template

    def test_user_matches_view(self):
        self.client.force_login(self.user)  # logging in user
        self.url = reverse("app_users:user-matches")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_matches.html")
        self.assertEqual(response.context["user"], self.user)
        self.assertQuerysetEqual(
            response.context["user_matches"],
            self.user.get_matches(),
            transform=lambda x: x,
        )

    def test_get_with_valid_match(self):
        other_user = User.objects.create(
            username="quirk-unicorn2",
            password="!passw@rd1232",
            first_name="John2",
            last_name="Doe2",
            email="john.doe@example.com2",
            info_about="I like to collect rubber ducks2",
            info_birthday=date(2000, 1, 1),
            info_gender="male",
            location_city="Rainbow City2",
            location_latitude=0,
            location_longitude=0,
            social_instagram="https://www.instagram.com/quirk_unicorn/",
            social_facebook="https://www.facebook.com/quirk_unicorn/",
            social_twitter="https://www.twitter.com/quirk_unicorn/",
            social_spotify="https://www.spotify.com/quirk_unicorn/",
        )
        match_object = UserMatch.objects.create(
            user=self.user, other=other_user, chatroom_uuid=uuid.uuid4()
        )
        self.client.force_login(self.user)

        # attempt to access profile of a non-matching user
        url = reverse(
            "app_users:user-match-profile-details",
            kwargs={"username": other_user.username},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/match_profile_details.html")
        self.assertEqual(response.context["user"], other_user)

        # attempt to access profile of a non-matching user
        url = reverse(
            "app_users:user-match-profile-details",
            kwargs={"username": "DOESNOTEXIST"},
        )
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_users:user-matches"))

    @mock.patch("app_users.views.celery_send_mail")
    def test_user_deletion(self, mock_email):
        mock_email.return_value = "Success"
        # define URL
        self.url = reverse("app_users:user-profile-delete")

        # make sure the user is logged in:
        self.client.force_login(self.user)

        user_id_before_deletion = self.user.id

        # Test GET request with valid form data
        response = self.client.get(
            self.url,
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code

        # check that the user is not present anymore in database
        try:
            user_object = User.objects.get(pk=user_id_before_deletion)
        except User.DoesNotExist:
            user_object = None

        self.assertEqual(user_object, None)
