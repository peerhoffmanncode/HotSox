from django.db.models import Q
from app_users.models import Sock, SockLike

import random


class PrePredictionAlgorithm:
    """basic preprediction algorithm for hotsox
    a next sock should be predicted for the pool of given socks
    """

    @staticmethod
    def get_next_sock(current_user_sock: Sock) -> Sock:
        """currently this method is a simple mockup of the later version!
        It is used to give a random record (sock) from the remaining pool of
        unseen socks. We use basic randomization for that - nothing fancy!
        """

        # get the queryset of all socks
        all_socks = Sock.objects.all()

        # get a queryset of all the unseen socks
        processed_socks = (
            SockLike.objects.filter(Q(like__isnull=False) | Q(dislike__isnull=False))
            .filter(sock=current_user_sock)
            .values_list("like", "dislike")
        )
        # create list of all the pks of the unseen socks
        processed_socks_pks = [
            sock_pk for sock_like in processed_socks for sock_pk in sock_like if sock_pk
        ]
        # exclude all the seen socks from the list of all the socks
        unseen_socks = all_socks.exclude(pk__in=processed_socks_pks)

        # check if there are remaining socks
        if unseen_socks:
            return unseen_socks[random.randint(0, len(unseen_socks) - 1)]

        # no reaming socks - return None!
        return None
