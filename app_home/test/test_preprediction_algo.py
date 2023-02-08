from django.test import TestCase
from app_users.models import User, UserMatch, Sock, SockLike
from datetime import date, timedelta
from app_home.pre_prediction_algorithm import PrePredictionAlgorithm


class Test(TestCase):
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
            email="quirk-unicorn1@example.com",
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

        self.sock = Sock.objects.create(
            user=self.user1,
            info_joining_date=date.today() - timedelta(days=365 * 5),
            info_name="Fuzzy Wuzzy 1",
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
            user=self.user1,
            info_joining_date=date.today() - timedelta(days=365 * 3),
            info_name="Fuzzy Wuzzy 2",
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

        self.sock3 = Sock.objects.create(
            user=self.user2,
            info_joining_date=date.today() - timedelta(days=365 * 5),
            info_name="Unicorn Fart 1",
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

        self.sock4 = Sock.objects.create(
            user=self.user2,
            info_joining_date=date.today() - timedelta(days=365 * 3),
            info_name="Unicorn Fart 2",
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

    def test_PrePredictionAlgorithm_prefilter_remainig_socks(self):
        list_of_unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            self.user1, self.sock
        )

        # socks in the list
        self.assertEqual([self.sock3, self.sock4], list(list_of_unseen_socks))
        # socks not in the list
        self.assertNotEqual([self.sock, self.sock2], list(list_of_unseen_socks))

    def test_PrePredictionAlgorithm_prefilter_remaining_socks_after_like(self):
        # like sock 3 - so only sock4 should be left
        SockLike.objects.create(sock=self.sock, like=self.sock3)
        # get remaining socks
        list_of_unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            self.user1, self.sock
        )

        self.assertEqual([self.sock4], list(list_of_unseen_socks))

    def test_PrePredictionAlgorithm_prefilter_remaining_socks_after_dislike(self):
        # dislike sock 3 - so only sock4 should be left
        SockLike.objects.create(sock=self.sock, dislike=self.sock3)
        # get remaining socks
        list_of_unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            self.user1, self.sock
        )

        self.assertEqual([self.sock4], list(list_of_unseen_socks))

    def test_PrePredictionAlgorithm_prefilter_no_remaining_socks(self):
        # dislike sock 3 - so only sock4 should be left
        SockLike.objects.create(sock=self.sock, dislike=self.sock3)
        # like sock 4 - no sock should remain
        SockLike.objects.create(sock=self.sock, like=self.sock4)
        # get remaining socks
        list_of_unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            self.user1, self.sock
        )

        self.assertEqual([], list(list_of_unseen_socks))

    # Only do this test if we decide on the fact that if one sock of a user was match,
    # all the other socks of the user will not be shown for further matches.
    # def test_PrePredictionAlgorithm_prefilter_no_socks_after_user_match(self):
    #     UserMatch.objects.create(user=self.user1, other=self.user2)
    #     list_of_unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
    #         self.user1, self.sock
    #     )
    #     self.assertEqual([], list(list_of_unseen_socks))
