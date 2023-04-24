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
from ..controller import ctr_user_pic

import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user",
    tags=["User ProfilePic"],
)


##
## Image
##
@router.post(
    "/profilepic",
    status_code=201,
    dependencies=[Depends(oauth2.check_active)],
)
@limiter.limit("20/minute")
async def add_user_profile_picture(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user_pic.create_user_pic(current_user.username, file, db)


@router.delete(
    "/profilepic/{id}", status_code=204, dependencies=[Depends(oauth2.check_active)]
)
@limiter.limit("20/minute")
async def delete_user_profile_picture(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user_pic.delete_user_pic(current_user.username, id, db)
