import random
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from sqlalchemy import func, or_, and_, not_
from sqlalchemy.orm import aliased
from api.database.models import User, Sock, SockLike, UserMatch
from api.database.setup import get_db_session


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
        db = get_db_session()
        all_none_user_socks = (
            db.query(Sock).filter(Sock.user_id != current_user.id).all()
        )
        all_seen_socks = [
            sock.dislike if sock.dislike is not None else sock.like
            for sock in db.query(SockLike)
            .filter(SockLike.sock_id == current_user_sock.id)
            .all()
        ]
        unwanted_user_list = [
            match.user if match.user != current_user else match.other
            for match in current_user.get_unmatched(db, current_user)
        ]

        unseen_socks = [
            sock for sock in all_none_user_socks if not sock in all_seen_socks
        ]

        # exclude all the socks without any pictures & unwanted users
        unseen_socks = [
            sock
            for sock in unseen_socks
            if sock.profile_pictures and sock.user_id not in unwanted_user_list
        ]

        # #### DEEEBUUUUUGGG ####
        # print("****************************************************************")
        # print(current_user, current_user_sock)
        # print("****************************************************************")
        # print("all_user_socks : ", len(current_user.socks))
        # for s in current_user.socks:
        #     print("all_none_user_sock:", s)

        # print("****************************************************************")
        # print("all_none_user_socks : ", len(all_none_user_socks))
        # for s in all_none_user_socks:
        #     print("all_none_user_sock:", s)

        # print("****************************************************************")
        # print("all_seen_socks : ", len(all_seen_socks))
        # for s in all_seen_socks:
        #     print("all_seen_sock:", s)

        # print("****************************************************************")
        # print("all unseen socks : ", len(unseen_socks))
        # for s in unseen_socks:
        #     print("unseen_sock:", s, s.user_id)

        # print("****************************************************************")
        # print("all unwanted_user_list : ", len(unwanted_user_list))
        # for s in unwanted_user_list:
        #     print("unseen_sock:", s)

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
                print(challenger_sock, score)
                # detect if sock is better match then current best
                if score > max_score:
                    max_score = score
                    chosen_one = challenger_sock

            # this is the currently simplest version of a pre-prediction: randomizing
            return chosen_one

        # no reaming socks - return None!
        return None
