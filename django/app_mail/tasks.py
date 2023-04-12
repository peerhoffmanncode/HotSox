from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task(name="send_email_in_background")
def celery_send_mail(email_subject, email_message: str, recipient_list: list, notification: bool):
    if notification == True:
        return send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )