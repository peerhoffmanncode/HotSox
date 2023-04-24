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
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

# load database
from ..database.setup import get_db
from ..database import models, schemas

# load authentication
from ..authentication import oauth2

# load business logic
from ..controller import ctr_chat

import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user", tags=["User Chats"]
)


##
## Chat
##
@router.get(
    "/chats",
    response_model=Page[schemas.MessageChatWithSender],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("10/minute")
async def get_all_chats(
    request: Request,
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return paginate(ctr_chat.show_all_chats(current_user.username, db), params)


@router.get(
    "/chat/{receiver}",
    response_model=list[schemas.MessageChatWithSender],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("30/minute")
async def get_chats(
    request: Request,
    receiver: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.show_specific_chat(current_user.username, receiver, db)


@router.post(
    "/chat/{receiver}",
    response_model=schemas.MessageChatWithSender,
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("30/minute")
async def send_chats(
    request: Request,
    receiver: str,
    chat_message: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.send_specific_chat(
        current_user.username, receiver, chat_message, db
    )
