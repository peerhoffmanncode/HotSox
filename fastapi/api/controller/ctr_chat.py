from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..database import models
from fastapi import HTTPException, status


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

    chats = (
        db.query(models.MessageChat)
        .filter((models.MessageChat.user == user) | (models.MessageChat.other == user))
        .all()
    )
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
    if user == other:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver and sender are the same <{receiver}>, you can not chat with yourself!",
        )
    chats = (
        db.query(models.MessageChat)
        .filter(
            or_(
                and_(
                    models.MessageChat.user == user, models.MessageChat.other == other
                ),
                and_(
                    models.MessageChat.user == other, models.MessageChat.other == user
                ),
            )
        )
        .all()
    )
    if not chats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No chats available between user <{username}> and <{receiver}>",
        )
    return chats


def send_specific_chat(username: str, receiver: str, chat_message: str, db: Session):
    """Business logic to show all chats for specific user"""
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
    if user == other:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver and sender are the same <{receiver}>, you can not chat with yourself!",
        )

    match = (
        db.query(models.UserMatch)
        .filter(
            (
                (models.UserMatch.user_id == other.id)
                & (models.UserMatch.other_id == user.id)
            )
            | (
                (models.UserMatch.user_id == user.id)
                & (models.UserMatch.other_id == other.id)
            )
        )
        .first()
    )
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You have no match with the user <{receiver}>!",
        )

    chat = models.MessageChat(user_id=user.id, other_id=other.id, message=chat_message)
    db.add(chat)
    db.commit()
    db.refresh(chat)

    # TODO: possible integration of WEBSOCKET support here
    return chat
