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
from ..controller import ctr_chat

import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/api") + "/user", tags=["User Chats"]
)


##
## Chat
##
@router.get(
    "/chats",
    response_model=list[schemas.MessageChatWithSender],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_all_chats(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.show_all_chats(current_user.username, db)


@router.get(
    "/chat/{receiver}",
    response_model=list[schemas.MessageChatWithSender],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
async def get_chats(
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
async def get_chats(
    receiver: str,
    chat_message: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.send_specific_chat(
        current_user.username, receiver, chat_message, db
    )
