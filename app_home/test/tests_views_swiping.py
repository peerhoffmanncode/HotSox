from django.test import TestCase
from app_users.models import User, Sock, SockLike
from datetime import date, timedelta

from django.urls import reverse

from importlib import import_module
from django.conf import settings as django_settings


class Test(TestCase):
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
        # create test user
        self.user = User.objects.create(
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

        self.sock2 = Sock.objects.create(
            user=self.user,
            info_joining_date=date.today() - timedelta(days=365 * 5),
            info_name="Wuzzy Fuzzy",
            info_about="Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
            info_color="7",
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

    def test_swipe_page_without_sock(self):
        # log user in
        self.client.force_login(user=self.user)

        # navigate to a certain route
        response = self.client.get(reverse("app_home:swipe"))

        # check if the user can see the swipepage without any sock selected
        self.assertEqual(response.status_code, 302)

    def test_swipe_page_with_sock_selected(self):

        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)

        # log user in
        self.client.force_login(user=self.user)

        # navigate to a certain route
        response = self.client.get(reverse("app_home:swipe"))

        # check if the user can see the swipepage without any sock selected
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("app_user/swipe.html")

    def test_swipe_page_with_sock_selected_like_sock(self):

        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)

        # log user in
        self.client.force_login(user=self.user)

        context = {"sock_pk": self.sock2.pk, "decision": "like"}

        # navigate to a certain route
        response = self.client.post(reverse("app_home:swipe"), data=context)

        # sock_likes = SockLike.objects.get(sock=self.sock)
        self.assertEqual(len(self.sock.get_likes()), 1)

        # check if the user can see the swipepage without any sock selected
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("app_user/swipe.html")

    def test_swipe_page_with_sock_selected_dislike_sock(self):

        session = self.get_session()
        session["sock_pk"] = self.sock.pk
        session.save()
        self.set_session_cookies(session)

        # log user in
        self.client.force_login(user=self.user)

        context = {"sock_pk": self.sock2.pk, "decision": "dislike"}

        # navigate to a certain route
        response = self.client.post(reverse("app_home:swipe"), data=context)

        # sock_likes = SockLike.objects.get(sock=self.sock)
        self.assertEqual(len(self.sock.get_dislikes()), 1)

        # check if the user can see the swipepage without any sock selected
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("app_user/swipe.html")
