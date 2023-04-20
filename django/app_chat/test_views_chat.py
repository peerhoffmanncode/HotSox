from django.test import TestCase
from app_users.models import User, UserMatch, MessageChat
from datetime import date, timedelta

from django.urls import reverse

from importlib import import_module
from django.conf import settings as django_settings

import uuid


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
        self.user1 = User.objects.create(
            username="quirk-unicorn 1",
            email="quirk-unicorn1@example.com",
            password="testpassword",
            first_name="Quirk1",
            last_name="Unicorn1",
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
            username="quirk-unicorn 2",
            email="quirk-unicorn2@example.com",
            password="p4ssword",
            first_name="Quirky2",
            last_name="Unicorn2",
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

    def test_no_chat_with_none_existing_user(self):
        # log user in
        self.client.force_login(user=self.user1)
        # navigate to a certain route
        response = self.client.get(
            reverse("app_chat:chat", kwargs={"matched_user_name": "DOESNOTEXIST"})
        )

        # check if the user can not see the chat page if not matched
        # should be redirected to matches
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/user/profile/matches/")

    def test_no_chat_with_no_match(self):
        # log user in
        self.client.force_login(user=self.user1)
        # navigate to a certain route
        response = self.client.get(
            reverse("app_chat:chat", kwargs={"matched_user_name": self.user2.username})
        )

        # check if the user can not see the chat page if not matched
        # should be redirected to matches
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/user/profile/matches/")

    def test_chat_with_match(self):
        # create a match
        user_match_object = UserMatch.objects.create(
            user=self.user1,
            other=self.user2,
            chatroom_uuid=uuid.uuid4(),
        )

        # log user in
        self.client.force_login(user=self.user1)
        # navigate to a certain route
        response = self.client.get(
            reverse("app_chat:chat", kwargs={"matched_user_name": self.user2.username})
        )

        # check if the user can not see the chat page if not matched
        # should be redirected to matches
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("app_chat/chat_lobby.html")

    def test_chat_with_very_many_old_chats(self):
        # create a match
        user_match_object = UserMatch.objects.create(
            user=self.user1,
            other=self.user2,
            chatroom_uuid=uuid.uuid4(),
        )

        # create chats
        for i in range(200):
            MessageChat.objects.create(
                user=self.user1, other=self.user2, message="Test!"
            )
        for i in range(200):
            MessageChat.objects.create(
                user=self.user2, other=self.user1, message="Test!"
            )

        # log user in
        self.client.force_login(user=self.user1)
        # navigate to a certain route
        response = self.client.get(
            reverse("app_chat:chat", kwargs={"matched_user_name": self.user2.username})
        )

        # check if chats are maxed @ 300
        # check if chats for the "other user" are set to seen
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("app_chat/chat_lobby.html")
        self.assertEqual(len(response.context["all_chats"]), 300)
        # my chat is not been seen yet!
        self.assertEqual(response.context["all_chats"][0].seen_date, None)
        # I have seen this chat!
        self.assertNotEqual(response.context["all_chats"][299].seen_date, None)
