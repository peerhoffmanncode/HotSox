from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

# how to call this function?
# celery_send_mail.apply_async(
#     kargs={
#         "email_subject": "some nice subject",
#         "email_message": "some nice message",
#         "recipient_list": ["some@list.de"],
#     }
# )
#
# or the easy/ convenient way
#
# celery_send_mail.delay(
#     email_subject="some nice subject",
#     email_message="some nice message",
#     recipient_list=["some@list.de"],
# )


@shared_task
def celery_send_mail(email_subject, email_message: str, recipient_list: list):
    return send_mail(
        subject=email_subject,
        message=email_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )
