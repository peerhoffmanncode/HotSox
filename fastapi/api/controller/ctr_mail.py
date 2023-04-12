import os
from sqlalchemy.orm import Session
from ..database import models, schemas
from fastapi import HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from celery_app import (
    celery_send_mail_to_user,
    celery_send_mail_to_all,
    celery_send_mail_to_all_fanout,
)


def fastapi_send_mail_background_task(
    background_tasks: BackgroundTasks, message: MessageSchema
):
    """utility function to send an email in a background task"""
    # build eMail Config
    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=int(os.getenv("MAIL_PORT")),
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        # TEMPLATE_FOLDER="./templates/email",
    )

    # send the mail in the background
    background_tasks.add_task(FastMail(conf).send_message, message)


##
## Mail
##
def show_all_mails(username: str, db: Session):
    """Business logic to show all mails in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )
    mails = db.query(models.MessageMail).filter(models.MessageMail.user == user).all()
    if not mails:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No mail available for user <{username}>",
        )

    return mails


async def send_mail_background(
    background_tasks: BackgroundTasks,
    username: str,
    message_body: schemas.MessageMailSending,
    db: Session,
):
    """Business logic to send a mail to specific user and store it to db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )
    try:
        # build eMail Schema
        message = MessageSchema(
            subject=message_body.dict().get("subject", "A email from hotsox"),
            recipients=[user.email],
            body=message_body.dict().get("content", "A email from hotsox"),
            subtype="html",
        )
        # fastapi_send_mail_background_task(background_tasks, message)

        celery_send_mail_to_user.delay(
            email=user.email,
            subject=message_body.dict().get(
                "subject", "eMail form then Hotsox project fastapi"
            ),
            content=message_body.dict().get(
                "content",
                "sad things happen, we miss some important message this time! stay safe and believe in the unicorn!",
            ),
        )

        # create db object
        new_mail = models.MessageMail(user_id=user.id, **message_body.dict())
        # write to db / commit!
        db.add(new_mail)
        db.commit()
        db.refresh(new_mail)
        return JSONResponse(
            status_code=200,
            content={"status": "email has been sent", "email": message_body.dict()},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email to <{user.username}>, <{user.email}>, {e}",
        )


def delete_mail(username: str, id: int, db: Session):
    """Business logic to delete specific mail in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )

    mail = db.query(models.MessageMail).filter(models.MessageMail.id == id).first()
    if not mail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This mail with id <{id}> is not available for user <{username}>",
        )
    if not mail in user.mail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username <{username}> doesn't have access to this mail",
        )

    db.delete(mail)
    db.commit()
    return {"success": f"Mail {id} was deleted"}
