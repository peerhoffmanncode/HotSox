from sqlalchemy.orm import Session
from ..database import models
from fastapi import HTTPException, status



def get_all_matches(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    all_matches = (
        db.query(models.UserMatch)
        .filter(
            (models.UserMatch.user_id == user.id)
            | (models.UserMatch.other_id == user.id)
        )
        .all()
    )
    if not all_matches:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User <{user.username}> has no matches",
        )

    return all_matches


def get_match(username: str, id: int, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    match = (
        db.query(models.UserMatch)
        .filter(
            (models.UserMatch.user_id == user.id)
            | (models.UserMatch.other_id == user.id)
        )
        .filter(models.UserMatch.id == id)
        .first()
    )
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specific match <{id}> for user <{user.username}> is not available!",
        )

    return match


def delete_match(username: str, id: int, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    # find valid match
    match = db.query(models.UserMatch).filter(models.UserMatch.id == id).first()
    if not match or (match.user_id != user.id and match.other_id != user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specific match <{id}> for user <{user.username}> is not available!",
        )

    if match.unmatched == True:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specific match <{id}> for user <{user.username}> is already unmatched!",
        )

    # set match to unmatched
    match.unmatched = True
    db.add(match)
    db.commit()
    db.refresh(match)

    if match.user_id == user.id:
        matched_user = match.other
    else:
        matched_user = match.user

    # delete dangling chats
    chats = (
        db.query(models.MessageChat)
        .filter(
            (
                (models.MessageChat.user_id == user.id)
                | (models.MessageChat.other_id == matched_user.id)
            )
            | (
                (models.MessageChat.user_id == matched_user.id)
                | (models.MessageChat.other_id == user.id)
            )
        )
        .all()
    )
    if chats:
        [db.delete(chat) for chat in chats]
        db.commit()

    return match
