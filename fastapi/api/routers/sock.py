from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_sock

import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/api") + "/user/sock", tags=["Socks"]
)


@router.get(
    "s/",
    response_model=list[schemas.ShowSock],
    dependencies=[Depends(oauth2.check_active)],
)
async def get_all_user(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.show_all(db)


@router.get(
    "/{id}",
    response_model=schemas.ShowSock,
    dependencies=[Depends(oauth2.check_active)],
)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_sock.show_specific(current_user.username, id, db)


# @router.post("/", response_model=schemas.ShowUser)
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     return create(request, db)
