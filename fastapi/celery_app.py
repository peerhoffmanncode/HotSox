import datetime
import logging
import time
import os

import celery

from task_lock import no_parallel_processing_of_task

LOGGER = logging.getLogger(__name__)

celery_app = celery.Celery(
    __name__,
)
celery_app.conf.broker_transport_options = {
    "visibility_timeout": datetime.timedelta(minutes=15).total_seconds()
}
celery_app.conf.task_acks_late = True
celery_app.conf.task_reject_on_worker_lost = True
celery_app.conf.worker_prefetch_multiplier = 1


@celery_app.task(name="send_mail_to_all")
def send_mail_to_all(user_list):
    for user in user_list:
        LOGGER.info(f"Sending newsletter to {user.email}")
        time.sleep(1)


@celery_app.task(name="send_mail_to_user")
def send_mail_to_user(user):
    LOGGER.info(f"Sending newsletter to {user.email}")
    time.sleep(1)


@celery_app.task(name="send_mail_to_all_fanout")
def send_mail_to_all_fanout(user_list):
    for user in user_list:
        send_mail_to_user.apply_async(kwargs={"user_email": user.email})


BATCH_SIZE = 2

# @celery_app.task(
#     name="send_newsletter_batching",
# )
# def send_newsletter_batching(last_evaluated_key=None):
#     last_evaluated_key = last_evaluated_key or -1
#     session = SessionLocal()
#     users = (
#         session.query(User)
#         .filter(User.id > last_evaluated_key)
#         .order_by(User.id)
#         .limit(BATCH_SIZE)
#         .all()
#     )

#     for user in users:
#         LOGGER.info(f"Sending newsletter to {user.email}")
#         time.sleep(1)

#     if len(users) < BATCH_SIZE:
#         return
#     new_last_evaluated_key = users[-1].id
#     send_newsletter_batching.apply_async(
#         kwargs={"last_evaluated_key": new_last_evaluated_key}
#     )


@celery_app.task(name="send_mail_to_all_locking", bind=True)
@no_parallel_processing_of_task
def send_mail_to_all_locking(user_list):
    for user in user_list:
        LOGGER.info(f"Sending newsletter to {user.email}")
        time.sleep(1)
