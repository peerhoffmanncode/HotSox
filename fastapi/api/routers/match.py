from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_match


import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/api") + "/user/match", tags=["Matches"]
)


@router.get(
    "es/",
    response_model=list[schemas.UserMatch],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_all_user_matches(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_match.get_all_matches(current_user.username, db)


@router.get(
    "/{id}",
    response_model=schemas.UserMatch,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_specific_user_match(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_match.get_match(current_user.username, id, db)


@router.post(
    "/{id}",
    response_model=schemas.UserMatch,
    dependencies=[Depends(oauth2.check_active)],
    status_code=202,
)
async def delete_specific_user_match(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_match.delete_match(current_user.username, id, db)
