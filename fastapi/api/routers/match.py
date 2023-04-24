from fastapi import APIRouter, Depends, status, Request
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_match

import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user/match",
    tags=["Matches"],
)


@router.get(
    "es/",
    response_model=Page[schemas.UserMatch],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("20/minute")
async def get_all_user_matches(
    request: Request,
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return paginate(ctr_match.get_all_matches(current_user.username, db), params)


@router.get(
    "/{id}",
    response_model=schemas.UserMatch,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("20/minute")
async def get_specific_user_match(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_match.get_match(current_user.username, id, db)


@router.delete(
    "/{id}",
    dependencies=[Depends(oauth2.check_active)],
    status_code=204,
)
@limiter.limit("20/minute")
async def delete_specific_user_match(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_match.delete_match(current_user.username, id, db)
