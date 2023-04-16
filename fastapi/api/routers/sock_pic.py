from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    File,
    UploadFile,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

# load database
from ..database.setup import get_db
from ..database import models, schemas

# load authentication
from ..authentication import oauth2

# load business logic
from ..controller import ctr_sock_pic

import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/fastapi/v1") + "/user/sock",
    tags=["Sock ProfilePic"],
)


##
## Image
##
@router.post(
    "/{sock_id}/profilepic",
    status_code=201,
    dependencies=[Depends(oauth2.check_active)],
)
async def add_user_profile_picture(
    sock_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock_pic.create_sock_pic(current_user.username, sock_id, file, db)


@router.delete(
    "/{sock_id}/profilepic/{pic_id}",
    status_code=204,
    dependencies=[Depends(oauth2.check_active)],
)
async def delete_user_profile_picture(
    sock_id: int,
    pic_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock_pic.delete_sock_pic(current_user.username, sock_id, pic_id, db)
