from sqlalchemy.orm import Session
from sqlalchemy import exc
from ..database import models, schemas
from fastapi import HTTPException, status
from ..authentication.hashing import Hash


##
## Users
##
def show_all_user(db: Session):
    """Business logic to show all users in db"""
    users = db.query(models.User).order_by(models.User.id.desc()).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No users available",
        )
    return users


def show_specific_user(username: str, db: Session):
    """Business logic to show specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username {username} is not available",
        )
    return user


def create_user(request: schemas.CreateUser, db: Session):
    """Business logic to create specific user in db"""

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
    """Business logic to edit specific user in db"""
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


def delete_user(username: str, db: Session):
    """Business logic to delete specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available!",
        )

    # delete the user with custom method
    user.delete(db)
    db.commit()
    return {"message": f"Success! User <{username}> was deleted!"}
