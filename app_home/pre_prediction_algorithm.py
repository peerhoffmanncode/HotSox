from django.db.models import Q
from app_users.models import Sock, SockLike

import random


class PrePredictionAlgorithm:
    """basic preprediction algorithm for hotsox
    a next sock should be predicted for the pool of given socks
    """

    @staticmethod
    def _prefilter_list_of_all_socks(current_user, current_user_sock: Sock) -> list:
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

        # get the queryset of all available socks
        all_socks = Sock.objects.all()

        # exclude all the seen socks from the list of all the socks
        # including the socks of the current user
        unseen_socks = all_socks.exclude(pk__in=processed_socks_pks).exclude(
            user=current_user
        )

        if unseen_socks:
            return unseen_socks
        return []

    @staticmethod
    def get_next_sock(current_user, current_user_sock: Sock) -> Sock:
        """currently this method is a simple mockup of the later version!
        It is used to give a random record (sock) from the remaining pool of
        unseen socks. We use basic randomization for that - nothing fancy!
        """

        # remaining unseen socks as list
        unseen_socks = PrePredictionAlgorithm._prefilter_list_of_all_socks(
            current_user, current_user_sock
        )

        # TODO ADD PROPER SELECTION ALGORITHM HERE
        # check if there are remaining socks
        if unseen_socks:
            # this is the currently simplest version of a pre-prediction: randomizing
            return unseen_socks[random.randint(0, len(unseen_socks) - 1)]

        # no reaming socks - return None!
        return None
