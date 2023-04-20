import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import models
from fastapi import HTTPException, status

from api.utilities.pre_prediction_algorithm import PrePredictionAlgorithm


def get_next_sock(username: str, id: int, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )
    current_sock = db.query(models.Sock).filter(models.Sock.id == id).first()
    if not current_sock in user.socks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id <{id}> is not available!",
        )

    sock = PrePredictionAlgorithm.get_next_sock(db, user, current_sock)
    if not sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No more socks to swipe",
        )
    return sock


def judge_sock(
    username: str, user_sock_id: int, other_sock_id: int, judgement: bool, db: Session
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    current_user_sock = (
        db.query(models.Sock).filter(models.Sock.id == user_sock_id).first()
    )
    if not current_user_sock in user.socks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id <{user_sock_id}> is not one of your socks!",
        )

    other_sock = db.query(models.Sock).filter(models.Sock.id == other_sock_id).first()
    if not other_sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id <{other_sock_id}> is not available!",
        )
    elif other_sock in user.socks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You can not judge your own sock!",
        )

    already_liked = (
        db.query(models.SockLike)
        .filter(
            models.SockLike.sock_id == user_sock_id,
            or_(
                models.SockLike.like_id == other_sock_id,
                models.SockLike.dislike_id == other_sock_id,
            ),
        )
        .first()
    )
    if already_liked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id <{other_sock_id}> was already judged!",
        )

    # setting the judgement to db
    if not judgement:
        judge = models.SockLike(dislike_id=other_sock_id, sock_id=user_sock_id)
    else:
        judge = models.SockLike(like_id=other_sock_id, sock_id=user_sock_id)
    db.add(judge)
    db.commit()
    db.refresh(judge)

    # check if we have a match!
    # check if like happens from boths ends!
    successful_user_match1 = (
        db.query(models.SockLike)
        .filter(
            (
                (models.SockLike.sock_id == other_sock_id)
                & (models.SockLike.like_id == user_sock_id)
            )
        )
        .first()
    )
    successful_user_match2 = (
        db.query(models.SockLike)
        .filter(
            (
                (models.SockLike.sock_id == user_sock_id)
                & (models.SockLike.like_id == other_sock_id)
            )
        )
        .first()
    )

    # found a valid match!
    set_valid_match = None
    if successful_user_match1 and successful_user_match2:
        # find already existing match
        existing_match = (
            db.query(models.UserMatch)
            .filter(
                (
                    (models.UserMatch.user_id == user.id)
                    & (models.UserMatch.other_id == other_sock.user.id)
                )
                | (
                    (models.UserMatch.user_id == other_sock.user.id)
                    & (models.UserMatch.other_id == user.id)
                )
            )
            .first()
        )

        if not existing_match:
            set_valid_match = models.UserMatch(
                user_id=user.id,
                other_id=other_sock.user.id,
                chatroom_uuid=uuid.uuid4(),
                unmatched=False,
            )
            db.add(set_valid_match)
            db.commit()
            db.refresh(set_valid_match)

        if set_valid_match:
            return {"Message": "New match found", "Match": set_valid_match}

    return {"Message": "No new match found"}
