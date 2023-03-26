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
from ..controller import ctr_user

import os

# build routes
router = APIRouter(prefix=os.environ.get("API_URL", "/api") + "/user", tags=["Users"])


##
## User
##
@router.get("s/", response_model=list[schemas.ShowUser])
async def get_all_user(
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_all_user(db)


@router.get("/{username}", response_model=schemas.ShowUser)
async def get_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_specific_user(username, db)


@router.post("/", response_model=schemas.CreateUser, status_code=201)
async def singup_user(request: schemas.CreateUser, db: Session = Depends(get_db)):
    print(request)
    return ctr_user.create_user(request, db)


# TODO: needs permission handling
@router.put("/{username}", response_model=schemas.EditUser, status_code=202)
async def edit_user(
    username: str,
    request: schemas.EditUser,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.edit_user(username, request, db)


# TODO: needs permission handling
@router.delete("/", status_code=204)  # , response_model=schemas.SimplyUser)
async def delete_user(
    request: schemas.SimplyUser,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_user.delete_user(request, db)


##
## Image
##
# TODO: needs permission handling
@router.post("/{username}/profilepic", status_code=201)
async def add_user_profile_picture(
    username: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.create_user_pic(username, file, db)


# TODO: needs permission handling
@router.delete("/{username}/profilepic/{id}", status_code=204)
async def delete_user_profile_picture(
    username: str,
    id: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.delete_user_pic(username, id, db)


##
## Mail
##
@router.get("/mails/{username}", response_model=list[schemas.MessageMail])
async def get_all_mail(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_all_mails(username, db)


@router.post("/mail/{username}", response_model=schemas.MessageMailSending)
async def send_mail(
    background_tasks: BackgroundTasks,
    username: str,
    message_body: schemas.MessageMailSending,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return await ctr_user.send_mail_background(background_tasks, username, message_body, db)


##
## Chat
##
@router.get("/chats/{username}", response_model=list[schemas.MessageChat])
async def get_all_chats(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    all_chats = ctr_user.show_all_chats(username, db)
    return all_chats


@router.get("/chat/{username}/{receiver}", response_model=list[schemas.MessageChat])
async def get_chats(
    username: str,
    receiver: str,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return ctr_user.show_specific_chat(username, receiver, db)
