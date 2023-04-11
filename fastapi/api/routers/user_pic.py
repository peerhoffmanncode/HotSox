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
from ..controller import ctr_user_pic

import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/api") + "/user", tags=["User ProfilePic"]
)


##
## Image
##
@router.post(
    "/profilepic",
    status_code=201,
    dependencies=[Depends(oauth2.check_active)],
)
async def add_user_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user_pic.create_user_pic(current_user.username, file, db)


@router.delete(
    "/profilepic/{id}", status_code=204, dependencies=[Depends(oauth2.check_active)]
)
async def delete_user_profile_picture(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user_pic.delete_user_pic(current_user.username, id, db)
