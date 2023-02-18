from django.test import TestCase
from ..models import User, UserProfilePicture, UserMatch, Sock, MessageMail, MessageChat
from datetime import date
from unittest import mock
import uuid


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
            username="quirky_unicorn2",
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
        self.user3 = User.objects.create(
            username="quirk-unicorn3",
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

        self.sock1 = Sock.objects.create(
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
        self.sock2 = Sock.objects.create(
            user=self.user1,
            info_name="Test Sock2",
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

        self.mail1 = MessageMail.objects.create(
            user=self.user1, subject="test message 1", content="test"
        )
        self.mail2 = MessageMail.objects.create(
            user=self.user1, subject="test message 2", content="test"
        )
        self.chat1 = MessageChat.objects.create(
            user=self.user1, other=self.user2, message="test chat message 1"
        )
        self.chat2 = MessageChat.objects.create(
            user=self.user1, other=self.user2, message="test chat message 2"
        )
        self.user_match1 = UserMatch.objects.create(
            user=self.user1, other=self.user2, chatroom_uuid=uuid.uuid4()
        )
        self.user_match2 = UserMatch.objects.create(
            user=self.user1, other=self.user3, chatroom_uuid=uuid.uuid4()
        )

    @mock.patch("app_users.models.User.get_all_pictures")
    def test_get_all_pictures(self, mock_get_all_pictures):
        # Set the return value of the mock
        mock_get_all_pictures.return_value = [
            "www.cloudinary.com/testurl1",
            "www.cloudinary.com/testurl2",
        ]

        # Call the method you're testing
        result = self.user1.get_all_pictures()

        # Assert the result
        self.assertEqual(len(result), 2)

    @mock.patch("app_users.models.User.get_picture_urls")
    def test_get_picture_urls(self, mock_get_picture_urls):
        # Set the return value of the mock
        mock_get_picture_urls.return_value = [
            "www.cloudinary.com/testurl1",
            "www.cloudinary.com/testurl2",
        ]

        # Call the method you're testing
        result = self.user1.get_picture_urls()

        # Assert the result
        self.assertEqual(
            result, ["www.cloudinary.com/testurl1", "www.cloudinary.com/testurl2"]
        )

    def test_get_matches(self):
        matches = self.user1.get_matches()
        self.assertEqual(len(matches), 2)
        self.assertIn(self.user_match1, matches)
        self.assertIn(self.user_match2, matches)

    # test if gets the socks, working
    def test_get_socks(self):
        socks = self.user1.get_socks()
        self.assertEqual(len(socks), 2)
        self.assertIn(self.sock1, socks)
        self.assertIn(self.sock2, socks)

    # working
    def test_get_mail_messages(self):
        messages = self.user1.get_mail_messages()
        self.assertEqual(len(messages), 2)
        self.assertIn(self.mail1, messages)
        self.assertIn(self.mail2, messages)

    # working
    def test_get_chat_messages(self):
        messages = self.user1.get_chat_messages()
        self.assertEqual(len(messages), 2)
        self.assertIn(self.chat1, messages)
        self.assertIn(self.chat2, messages)
