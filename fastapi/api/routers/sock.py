from fastapi import APIRouter, Depends, status, Request
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_sock


import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user/sock", tags=["Socks"]
)


@router.get(
    "s/",
    response_model=Page[schemas.ShowSock],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("20/minute")
async def get_all_socks(
    request: Request,
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
@limiter.limit("30/minute")
async def get_sock(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.show_specific(current_user.username, id, db)


@router.post("/", response_model=schemas.ShowSock, status_code=201)
@limiter.limit("20/minute")
async def create_sock(
    request: Request,
    body: schemas.CreateUpdateSock,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.create_sock(current_user.username, body, db)


@router.put(
    "/{id}",
    response_model=schemas.ShowSock,
    status_code=202,
    dependencies=[Depends(oauth2.check_active)],
)
@limiter.limit("20/minute")
async def edit_sock(
    request: Request,
    id: int,
    body: schemas.CreateUpdateSock,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.edit_sock(current_user.username, id, body, db)


@router.delete(
    "/{id}", status_code=204, dependencies=[Depends(oauth2.check_active)]
)  # , response_model=schemas.SimplyUser)
@limiter.limit("20/minute")
async def delete_sock(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_sock.delete_sock(current_user.username, id, db)
