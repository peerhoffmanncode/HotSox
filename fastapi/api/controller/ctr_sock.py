from sqlalchemy.orm import Session
from ..database import models, schemas
from fastapi import HTTPException, status
from ..authentication.hashing import Hash


def show_all(db: Session):
    sock = db.query(models.Sock).all()
    if not sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sock available",
        )
    return sock


def show_specific(username: str, id: int, db: Session):
    query = db.query(models.Sock).join(models.User)
    sock = query.filter(
        models.User.username == username,
        models.Sock.id == id,
    ).first()

    if not sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with the id {id} is not available",
        )
    return sock


def create_sock(username: str, request: schemas.CreateUpdateSock, db: Session):
    """Business logic to create specific user in db"""

    # check for duplicates
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User already exists! <{request.dict()['username']}>",
        )

    # create db object
    new_sock = models.Sock(user_id=user.id, **request.dict())
    # write to db / commit!
    db.add(new_sock)
    db.commit()
    db.refresh(new_sock)
    return new_sock


def edit_sock(username: str, id: int, request: schemas.CreateUpdateSock, db: Session):
    """Business logic to edit specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username {username} is not available",
        )

    current_sock = (
        db.query(models.Sock)
        .filter(models.Sock.user_id == user.id, models.Sock.id == id)
        .first()
    )

    if not current_sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with id <{id}> for the user {username} is not available",
        )

    # check for duplicates
    db.query(models.Sock).filter(models.Sock.id == id).update(request.dict())
    db.commit()
    db.refresh(current_sock)
    return current_sock


def delete_sock(username: str, id: int, db: Session):
    """Business logic to delete specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    current_sock = (
        db.query(models.Sock)
        .filter(models.Sock.user_id == user.id, models.Sock.id == id)
        .first()
    )
    if not current_sock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sock with id <{id}> for the user {username} is not available",
        )
    # delete the user with custom method
    current_sock.delete(db)
    db.commit()
    return {"message": f"Success! Sock id <{id}> from user <{username}> was deleted!"}
