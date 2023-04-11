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
from ..controller import ctr_user, ctr_user_pic, ctr_mail, ctr_chat

import os

# build routes
router = APIRouter(prefix=os.environ.get("API_URL", "/api") + "/user", tags=["Users"])


##
## User
##
@router.get(
    "s/",
    response_model=list[schemas.ShowUser],
    dependencies=[Depends(oauth2.check_superuser)],
)
async def get_all_user(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_all_user(db)


@router.get(
    "/", response_model=schemas.ShowUser, dependencies=[Depends(oauth2.check_active)]
)
async def get_user(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_specific_user(current_user.username, db)


@router.post("/", response_model=schemas.CreateUser, status_code=201)
async def singup_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    return ctr_user.create_user(request, db)


@router.put(
    "/",
    response_model=schemas.EditUser,
    status_code=202,
    dependencies=[Depends(oauth2.check_active)],
)
async def edit_user(
    request: schemas.EditUser,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.edit_user(current_user.username, request, db)


# permission handling superuser!
@router.delete(
    "/", status_code=204, dependencies=[Depends(oauth2.check_superuser)]
)  # , response_model=schemas.SimplyUser)
async def delete_user(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_user.delete_user(current_user.username, db)


##
## Image
##
@router.post(
    "/profilepic", status_code=201, dependencies=[Depends(oauth2.check_active)]
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


##
## Mail
##
@router.get(
    "/mail",
    response_model=list[schemas.MessageMail_with_id],
    dependencies=[Depends(oauth2.check_active)],
)
async def get_all_mail(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_mail.show_all_mails(current_user.username, db)


@router.post(
    "/mail",
    response_model=schemas.MessageMail_with_id,
    dependencies=[Depends(oauth2.check_active)],
)
async def send_mail(
    background_tasks: BackgroundTasks,
    message_body: schemas.MessageMailSending,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return await ctr_mail.send_mail_background(
        background_tasks, current_user.username, message_body, db
    )


@router.delete(
    "/mail/{id}",
    dependencies=[Depends(oauth2.check_active)],
)
async def delete_mail(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_mail.delete_mail(current_user.username, id, db)


##
## Chat
##
@router.get(
    "/chats",
    response_model=list[schemas.MessageChat],
    dependencies=[Depends(oauth2.check_active)],
)
async def get_all_chats(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.show_all_chats(current_user.username, db)


@router.get(
    "/chat/{receiver}",
    response_model=list[schemas.MessageChat],
    dependencies=[Depends(oauth2.check_active)],
)
async def get_chats(
    receiver: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_chat.show_specific_chat(current_user.username, receiver, db)
