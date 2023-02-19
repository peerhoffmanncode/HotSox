from django.test import TestCase, Client
from django.test.client import RequestFactory
from unittest import mock

from importlib import import_module
from django.conf import settings as django_settings

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta

from ..models import User, Sock, SockProfilePicture
from ..views import validate_sock_ownership


class UserSignUpTest(TestCase):
    def get_session(self):
        if self.client.session:
            session = self.client.session
        else:
            engine = import_module(django_settings.SESSION_ENGINE)
            session = engine.SessionStore()
        return session

    def set_session_cookies(self, session):
        # Set the cookie to represent the session
        session_cookie = django_settings.SESSION_COOKIE_NAME
        self.client.cookies[session_cookie] = session.session_key
        cookie_data = {
            "max-age": None,
            "path": "/",
            "domain": django_settings.SESSION_COOKIE_DOMAIN,
            "secure": django_settings.SESSION_COOKIE_SECURE or None,
            "expires": None,
        }
        self.client.cookies[session_cookie].update(cookie_data)

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

        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)

    # validate_sock_ownership(request, valid_sock=None, picture_pk=None)
    @mock.patch("cloudinary.uploader.upload")
    def test_valid_picture_helper_method(self, mock_uploader_upload):

        mock_uploader_upload = "picture.jpg"
        self.picture = SockProfilePicture.objects.create(
            sock=self.sock, profile_picture="picture.jpg"
        )

        self.client.force_login(self.user)  # logging in user

        # test with a valid picture pk
        self.assertTrue(
            validate_sock_ownership(
                request=None, valid_sock=self.sock, picture_pk=self.picture.pk
            )
        )
        # test with an invalid picture pk
        self.assertFalse(
            validate_sock_ownership(request=None, valid_sock=self.sock, picture_pk=10)
        )
        # test with a valid sock belonging to the user
        request = self.client.request().wsgi_request
        self.assertTrue(validate_sock_ownership(request=request, valid_sock=self.sock))

        # test with an invalid sock not belonging to the user
        request = self.client.request().wsgi_request

        other_user = User.objects.create(username="otheruser", password="otherpass")
        other_sock = Sock.objects.create(
            user=other_user,
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
        self.assertFalse(
            validate_sock_ownership(request=request, valid_sock=other_sock)
        )

    def SockOverviewTest(self):
        self.client.force_login(self.user)
        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)
        response = self.client.get(reverse("app_users:sock-overview"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["left_arrow_go_to_url"],
            reverse("app_users:user-profile-update"),
        )
        self.assertEqual(response.context["right_arrow_go_to_url"], "")

        # create a sock to delete
        response = self.client.post(
            reverse("app_users:sock-overview"),
            {"method": "delete", "sock_pk": self.sock.pk},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app_users:sock-overview"))
        self.assertFalse(Sock.objects.filter(pk=self.sock.pk).exists())

        response = self.client.post(
            reverse("app_users:sock-overview"), {"method": "add"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app_users:sock-create"))

    def test_sock_selection(self):
        self.client.force_login(self.user)
        url = reverse("app_users:sock-selection")
        redirect_url = reverse("app_users:sock-details")

        # test a POST request without a sock pk
        response = self.client.post(
            url, data={"sock_pk": self.sock.pk, "redirect_url": redirect_url}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_url)
        self.assertEqual(self.client.session["sock_pk"], str(self.sock.pk))

        # test a POST request with a prev_url
        prev_url = reverse("app_users:user-signup")
        response = self.client.post(
            url, data={"sock_pk": self.sock.pk}, HTTP_REFERER=prev_url
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, prev_url)
        self.assertEqual(self.client.session["sock_pk"], str(self.sock.pk))

    def test_sock_profile_create_view(self):
        self.client.force_login(self.user)
        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)
        response = self.client.get(reverse("app_users:sock-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/sock_update.html")
        self.assertContains(response, "sock")

        data = {
            "user": self.user,
            "info_joining_date": date.today() - timedelta(days=365 * 5),
            "info_name": "Fuzzy Wuzzy",
            "info_about": "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
            "info_color": "5",
            "info_fabric": "2",
            "info_fabric_thickness": "7",
            "info_brand": "13",
            "info_type": "4",
            "info_size": "7",
            "info_age": 10,
            "info_separation_date": date.today() - timedelta(days=365),
            "info_condition": "9",
            "info_holes": 3,
            "info_kilometers": 1000,
            "info_inoutdoor": "1",
            "info_washed": 2,
            "info_special": "Once won first place in a sock puppet competition",
        }

        response = self.client.post(reverse("app_users:sock-create"), data)
        session = self.get_session()
        session["sock_pk"] = self.sock.pk + 1
        session.save()
        self.set_session_cookies(session)
        self.assertRedirects(
            response,
            reverse("app_users:sock-picture"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Sock.objects.count(), 2)

    def test_sock_detail_view(self):
        # check if detail view is forbidden if not logged in!
        response = self.client.get(reverse("app_users:sock-details"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)
        response = self.client.get(reverse("app_users:sock-details"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["left_arrow_go_to_url"], reverse("app_users:sock-overview")
        )
        self.assertEqual(
            response.context["right_arrow_go_to_url"],
            reverse("app_users:sock-update"),
        )
        self.assertTemplateUsed(response, "users/sock_details.html")

    def test_sock_profile_update_view_get(self):
        # check if update view is forbidden if not logged in!
        response = self.client.get(reverse("app_users:sock-update"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)

        response = self.client.get(reverse("app_users:sock-update"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/sock_update.html")
        self.assertContains(response, "sock")

        response = self.client.post(
            reverse("app_users:sock-update"),
            data={
                "user": self.user,
                "info_joining_date": date.today() - timedelta(days=365 * 5),
                "info_name": "Wacko Charlie",
                "info_about": "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
                "info_color": "5",
                "info_fabric": "2",
                "info_fabric_thickness": "7",
                "info_brand": "13",
                "info_type": "4",
                "info_size": "7",
                "info_age": 10,
                "info_separation_date": date.today() - timedelta(days=365),
                "info_condition": "9",
                "info_holes": 3,
                "info_kilometers": 1000,
                "info_inoutdoor": "1",
                "info_washed": 2,
                "info_special": "Once won first place in a sock puppet competition",
            },
        )
        self.assertRedirects(
            response,
            reverse("app_users:sock-details"),
            status_code=302,
            target_status_code=200,
        )
        updated_sock = Sock.objects.get(pk=self.sock.pk)
        self.assertEqual(updated_sock.info_name, "Wacko Charlie")

    @mock.patch("cloudinary.uploader.upload")
    def test_post_add_picture(self, mock_uploader_upload):
        # Set up mock return value for cloudinary.uploader.upload
        mock_uploader_upload = "picture.jpg"

        self.url = reverse("app_users:sock-picture")
        self.picture = SimpleUploadedFile(
            "picture.jpg", b"file_content", content_type="image/jpeg"
        )

        self.client.force_login(self.user)  # logging in user
        # add this sock to current session
        # Create a new SockProfilePictureForm with a picture file
        response = self.client.post(
            self.url,
            data={
                "method": "add",
                "profile_picture": self.picture,
            },
        )
        self.assertEqual(response.status_code, 302)  # check redirect status code
        self.assertEqual(response.url, self.url)  # check redirect url
        self.assertEqual(
            len(self.sock.get_all_pictures()), 1
        )  # check if picture is added to the user

        # test to delete a sock picture
        # Send a POST request to the view with the picture PK
        response = self.client.post(
            self.url,
            data={"picture_pk": self.sock.get_all_pictures()[0].pk, "method": "delete"},
        )

        # Assert that the view redirected to the correct URL
        self.assertRedirects(response, self.url)

        # Assert that the SockProfilePicture object was deleted
        self.assertEqual(len(self.sock.get_all_pictures()), 0)
