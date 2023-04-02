from allauth.account.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def signal_user_logged_in(request, **kwargs):
    # entry point to check status of user!
    # TODO: check
    # unseen matches
    # unseen chat messages
    pass
