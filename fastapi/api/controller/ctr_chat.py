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
## Chats
##
def show_all_chats(username: str, db: Session):
    """Business logic to show all chats for specific user"""
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
    """Business logic to show all chats between specific users"""
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
