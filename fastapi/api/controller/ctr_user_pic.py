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
## Profile pic
##
def create_user_pic(username: str, file: UploadFile, db: Session):
    """Business logic to create a profilepic for specific user in db"""
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
    """Business logic to delete a profilepic for specific user in db"""
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
    if not picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This picture with id <{id}> is not available for user <{username}>",
        )
    if not picture in user.profile_pictures:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username <{username}> doesn't have access to this picture",
        )

    picture.delete(db)
    db.commit()
    return {"success": f"picture {id} was deleted"}
