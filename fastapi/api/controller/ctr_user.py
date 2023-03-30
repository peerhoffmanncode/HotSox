import os
from sqlalchemy.orm import Session
from sqlalchemy import exc, or_
from ..database import models, schemas
from fastapi import HTTPException, status, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..authentication.hashing import Hash

from datetime import datetime

from cloudinary import api, uploader


##
## Users
##
def show_all_user(db: Session):
    users = db.query(models.User).order_by(models.User.id.desc()).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No users available",
        )
    return users


def show_specific_user(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username {username} is not available",
        )
    return user


def create_user(request: schemas.CreateUser, db: Session):
    # hash password before storing it to the db!
    request.password = Hash.encrypt(request.password)

    # check for duplicates
    user = (
        db.query(models.User)
        .filter(models.User.username == request.dict()["username"])
        .first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already exists! <{request.dict()['username']}>",
        )
    user = (
        db.query(models.User)
        .filter(models.User.email == request.dict()["email"])
        .first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"eMail address already exists! <{request.dict()['email']}>",
        )

    # create db object
    new_user = models.User(**request.dict())
    # write to db / commit!
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def edit_user(username: str, request: schemas.EditUser, db: Session):
    current_user = (
        db.query(models.User).filter(models.User.username == username).first()
    )
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username {username} is not available",
        )

    # check for duplicates
    try:
        db.query(models.User).filter(models.User.username == username).update(
            request.dict()
        )
        db.commit()
        db.refresh(current_user)
    except exc.IntegrityError as excep_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Already exists! <{e.orig}>",
        ) from excep_text
    return current_user


def delete_user(request: schemas.SimplyUser, db: Session):
    user = (
        db.query(models.User)
        .filter(
            models.User.username == request.username, models.User.email == request.email
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{request.username}> and email <{request.email}> is not available!",
        )

    # delete the user with custom method
    user.delete(db)
    db.commit()
    return {"message": f"Success! User <{request.username}> was deleted!"}


##
## Profile pic
##
def create_user_pic(username: str, file: UploadFile, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )

    upload_result = uploader.upload(file.file)
    if not upload_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upload error for file <{file.filename}>",
        )
    # get pucture url
    url = upload_result.get("url", None)
    # build image object
    picture = models.UserProfilePicture(profile_picture=url)
    # append picture to user
    user.profile_pictures.append(picture)
    # store changes to db
    db.add(user)
    db.commit()
    db.refresh(user)

    # return latest picture
    return user.profile_pictures[-1]


def delete_user_pic(username: str, id: int, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )

    picture = (
        db.query(models.UserProfilePicture)
        .filter(models.UserProfilePicture.id == id)
        .first()
    )
    if not picture in user.profile_pictures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username <{username}> doesn't have access to this picture",
        )

    picture.delete(db)
    db.commit()
    return {"success": f"picture {id} was deleted", "user": user.profile_pictures}


##
## Mail
##
def show_all_mails(username: str, db: Session):
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
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )
    try:
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

        # build eMail Schema
        message = MessageSchema(
            subject=message_body.dict().get("subject", "A email from hotsox"),
            recipients=[user.email],
            body=message_body.dict().get("content", "A email from hotsox"),
            subtype="html",
        )

        # send the mail in the background
        background_tasks.add_task(FastMail(conf).send_message, message)

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
            detail=f"Error sending email to <{user.username}>, <{user.email}>",
        )


##
## Chats
##
def show_all_chats(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )
    chats = db.query(models.MessageChat).filter(models.MessageChat.user == user).all()
    if not chats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chats available for user <{username}>",
        )

    return chats


def show_specific_chat(username: str, receiver: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )
    other = db.query(models.User).filter(models.User.username == receiver).first()
    if not other:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver with the username <{receiver}> is not available",
        )

    chats = (
        db.query(models.MessageChat)
        .filter(models.MessageChat.user == user, models.MessageChat.other == other)
        .all()
    )
    if not chats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chats available between user <{username}> and <{receiver}>",
        )
    return chats
