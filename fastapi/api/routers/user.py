from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    File,
    UploadFile,
    BackgroundTasks,
    Body,
    Request,
)
from fastapi_pagination import Page, Params, add_pagination, paginate

from sqlalchemy.orm import Session

# load database
from ..database.setup import get_db
from ..database import models, schemas

# load authentication
from ..authentication import oauth2

# load business logic
from ..controller import ctr_user

import os

from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user", tags=["User"]
)


##
## User
##
@router.get(
    "s/",
    response_model=Page[schemas.ShowUser],
    dependencies=[Depends(oauth2.check_superuser)],
)
@limiter.limit("10/minute")
async def get_all_user(
    request: Request,
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return paginate(ctr_user.show_all_user(db), params)


@router.get(
    "/", response_model=schemas.ShowUser, dependencies=[Depends(oauth2.check_active)]
)
@limiter.limit("20/minute")
async def get_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_specific_user(current_user.username, db)


@router.post("/", response_model=schemas.CreateUserOut, status_code=201)
async def singup_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    return ctr_user.create_user(request, db)


@router.put(
    "/",
    response_model=schemas.EditUserOut,
    status_code=202,
    dependencies=[Depends(oauth2.check_active)],
)
@limiter.limit("10/minute")
async def edit_user(
    request: Request,
    body: schemas.EditUser = Body(exclude_unset=True),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.edit_user(current_user.username, body, db)


# permission handling superuser!
@router.delete(
    "/", status_code=204, dependencies=[Depends(oauth2.check_superuser)]
)  # , response_model=schemas.SimplyUser)
@limiter.limit("10/minute")
async def delete_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_user.delete_user(current_user.username, db)
