from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from ..database.setup import get_db
from ..database import models, schemas

from ..authentication import oauth2

# load business logic
from ..controller import ctr_swipe


import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user/swipe", tags=["Swipe"]
)


@router.get(
    "/{user_sock_id}/next",
    response_model=schemas.ShowSock,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("30/minute")
async def get_next_sock(
    request: Request,
    user_sock_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_swipe.get_next_sock(current_user.username, user_sock_id, db)


@router.post(
    "/{user_sock_id}/judge/{other_sock_id}",
    # response_model=schemas.UserMatch,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("20/minute")
async def judge_a_sock(
    request: Request,
    judgement: bool,
    user_sock_id: int,
    other_sock_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_swipe.judge_sock(
        current_user.username, user_sock_id, other_sock_id, judgement, db
    )
