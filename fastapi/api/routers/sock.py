from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_sock


import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/fastapi/v1") + "/user/sock", tags=["Socks"]
)


@router.get(
    "s/",
    response_model=Page[schemas.ShowSock],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_all_socks(
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return paginate(ctr_sock.show_all(current_user.username, db), params)


@router.get(
    "/{id}",
    response_model=schemas.ShowSock,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_sock(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.show_specific(current_user.username, id, db)


@router.post("/", response_model=schemas.ShowSock, status_code=201)
async def create_sock(
    request: schemas.CreateUpdateSock,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.create_sock(current_user.username, request, db)


@router.put(
    "/{id}",
    response_model=schemas.ShowSock,
    status_code=202,
    dependencies=[Depends(oauth2.check_active)],
)
async def edit_sock(
    id: int,
    request: schemas.CreateUpdateSock,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.edit_sock(current_user.username, id, request, db)


# permission handling superuser!
@router.delete(
    "/{id}", status_code=204, dependencies=[Depends(oauth2.check_active)]
)  # , response_model=schemas.SimplyUser)
async def delete_sock(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_sock.delete_sock(current_user.username, id, db)
