from sqlalchemy.orm import Session
from ..database import models
from fastapi import HTTPException, status, UploadFile
from cloudinary import uploader


##
## Profile pic
##
def create_sock_pic(username: str, id: int, file: UploadFile, db: Session):
    """Business logic to create a profilepic for specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
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

    upload_result = uploader.upload(file.file)
    if not upload_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Upload error for file <{file.filename}>",
        )
    # get pucture url
    url = upload_result.get("url", None)
    # build image object
    picture = models.SockProfilePicture(profile_picture=url)
    # append picture to user
    current_sock.profile_pictures.append(picture)
    # store changes to db
    db.add(current_sock)
    db.commit()
    db.refresh(current_sock)

    # return latest picture
    return current_sock.profile_pictures[-1]


def delete_sock_pic(username: str, sock_id: int, pic_id: int, db: Session):
    """Business logic to delete a profilepic for specific user in db"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the username <{username}> is not available",
        )

    picture = (
        db.query(models.SockProfilePicture)
        .join(models.Sock)
        .filter(models.Sock.id == sock_id, models.SockProfilePicture.id == pic_id)
        .first()
    )
    if not picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This picture with id <{pic_id}> is not available for sock id <{sock_id}>",
        )

    picture.delete(db)
    db.commit()
    return {"success": f"picture {id} was deleted"}
