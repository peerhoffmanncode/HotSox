from __future__ import absolute_import, unicode_literals
import datetime
import os
from dotenv import load_dotenv

load_dotenv("../.env")
if os.environ.get("SECRET_KEY", None) is None:
    print("can not find env file!")
    exit(-1)

# from sqlalchemy.orm import Session
from celery import Celery
import yagmail
from cloudinary import uploader


# Setup celery app
celery_app = Celery(__name__)

# celery app configuration
celery_app.conf.broker_transport_options = {
    "visibility_timeout": datetime.timedelta(minutes=15).total_seconds()
}
celery_app.conf.task_acks_late = True
celery_app.conf.task_reject_on_worker_lost = True
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.broker_url = os.environ.get("REDIS_FASTAPI_URL")
celery_app.conf.result_backend = os.environ.get("REDIS_FASTAPI_URL")

# build eMail Config
awesome_yag = yagmail.SMTP(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))


@celery_app.task(name="send_mail_to_user")
def celery_send_mail_to_user(email: str, subject: str, content: str):
    awesome_yag.send(email, subject, content)
    return {"message": f"email was send to {email}"}


@celery_app.task(name="send_mail_to_all")
def celery_send_mail_to_all(emails: list, subject: str, content: str):
    for email in emails:
        awesome_yag.send(email, subject, content)
    return {"message": f"email was send to {emails}"}


@celery_app.task(name="send_mail_to_all_fanout")
def celery_send_mail_to_all_fanout(emails: list, subject: str, content: list):
    for email in emails:
        celery_send_mail_to_user(email, subject, content)
    return {"message": f"email was send to {emails}"}


@celery_app.task(name="destroy_profilepicture_on_cloud")
def destroy_profilepicture_on_cloud(public_id):
    uploader.destroy(public_id)
    return {"message": f"profile on cloud storage destroyed!"}
