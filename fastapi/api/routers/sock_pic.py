from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    File,
    UploadFile,
    BackgroundTasks,
    Request,
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
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user/sock",
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
@limiter.limit("20/minute")
async def add_user_profile_picture(
    request: Request,
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
@limiter.limit("20/minute")
async def delete_user_profile_picture(
    request: Request,
    sock_id: int,
    pic_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock_pic.delete_sock_pic(current_user.username, sock_id, pic_id, db)
