from django.db.models import Q
from app_users.models import User, Sock, SockLike, UserMatch
import random
from datetime import datetime, timedelta
from difflib import SequenceMatcher


class PrePredictionAlgorithm:
    """basic preprediction algorithm for hotsox
    a next sock should be predicted for the pool of given socks
    """

    @staticmethod
    def _compare_socks(current_sock, challenger_sock):
        """function to calculate a similarity score between two socks"""

        similarity_score = -1

        # Weightage of each attribute
        weights = {
            "info_color": 10,
            "info_size": 8,
            "info_type": 7,
            "info_fabric": 6,
            "info_condition": 6,
            "info_holes": 6,
            "info_age": 5,
            "info_fabric_thickness": 5,
            "info_kilometers": 4,
            "info_inoutdoor": 4,
            "info_washed": 4,
            "info_brand": 3,
            "info_joining_date": 5,
            "info_separation_date": 2,
            "info_special": 2,
            "info_about": 2,
        }
        # Maxima for percentage calculation
        maxima = {
            "info_color": 10,
            "info_size": 7,
            "info_type": 9,
            "info_fabric": 7,
            "info_condition": 12,
            "info_holes": 10,
            "info_age": 25,
            "info_fabric_thickness": 7,
            "info_kilometers": 1000,
            "info_inoutdoor": 9,
            "info_washed": 7,
            "info_brand": 12,
        }

        # Calculate similarity score for each attribute
        ratio = 1  # default ratio
        for attribute, weight in weights.items():
            # calculate for dates
            if attribute in ["info_joining_date", "info_separation_date"]:
                current_value = current_sock.__dict__.get(attribute)
                challenger_value = challenger_sock.__dict__.get(attribute)
                delta = abs((current_value - challenger_value).days)
                if delta <= 60:
                    ratio = (60 - delta) / 60
                else:
                    ratio = 0.1
                similarity_score += weight * ratio

            # calculate for text
            elif attribute in ["info_special", "info_about"]:
                current_value = current_sock.__dict__.get(attribute)
                challenger_value = challenger_sock.__dict__.get(attribute)
                ratio = SequenceMatcher(None, current_value, challenger_value).ratio()
                similarity_score += weight * ratio

            # calcualte for any other integer values
            else:
                ratio = (
                    1
                    - abs(
                        int(current_sock.__dict__.get(attribute))
                        - int(challenger_sock.__dict__.get(attribute))
                    )
                    / maxima[attribute]
                )
                similarity_score += weight * ratio

        # return final score
        return similarity_score

    @staticmethod
    def _prefilter_list_of_all_socks(
        current_user: User, current_user_sock: Sock
    ) -> list:
        """This method is used to pre filter the list of all socks to the currently
        useen ones and return a list. All the liked and disliked socks as well as the
        socks of the user him/herself are excluded from the list.
        """

        # get a queryset of all the unseen socks
        processed_socks = (
            SockLike.objects.filter(Q(like__isnull=False) | Q(dislike__isnull=False))
            .filter(sock=current_user_sock)
            .values_list("like", "dislike")
        )
        # create a list of all the pks of the unseen socks
        processed_socks_pks = [
            sock_pk for sock_like in processed_socks for sock_pk in sock_like if sock_pk
        ]

        # get the queryset of all available socks, but:
        # exclude all the seen socks from the list of all the socks (above)
        # exclude the socks of the current user too!
        unseen_socks = (
            Sock.objects.all()
            .exclude(pk__in=processed_socks_pks)
            .exclude(user=current_user)
        )

        # build a list of users that have been unmatched,
        # so that we can exclude their socks of the unseen socks!
        # TODO: could be extended to exclude socks of any matched user too!
        unwanted_user_list = [
            match.user if match.user != current_user else match.other
            for match in current_user.get_unmatched()
        ]

        # exclude all the socks without any pictures & unwanted users
        unseen_socks = [
            sock
            for sock in unseen_socks
            if sock.get_all_pictures() and sock.user not in unwanted_user_list
        ]

        if unseen_socks:
            return unseen_socks
        return []

    @staticmethod
    def get_next_sock(current_user, current_user_sock: Sock) -> Sock | None:
        """currently this method is a simple mockup of the later version!
        It is used to give a random record (sock) from the remaining pool of
        unseen socks. We use basic randomization for that - nothing fancy!
        """

        # remaining unseen socks as list
        unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            current_user, current_user_sock
        )

        # check if there are remaining socks
        if unseen_socks:
            max_score = -1
            chosen_one = unseen_socks[0]
            # find best contender for match
            for challenger_sock in unseen_socks:
                score = PrePredictionAlgorithm._compare_socks(
                    current_user_sock, challenger_sock
                )
                # detect if sock is better match then current best
                if score > max_score:
                    max_score = score
                    chosen_one = challenger_sock

            # this is the currently simplest version of a pre-prediction: randomizing
            return chosen_one

        # no reaming socks - return None!
        return None
