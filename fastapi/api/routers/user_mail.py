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
from ..controller import ctr_mail

import os

# build routes
router = APIRouter(
    prefix=os.environ.get("API_URL", "/api") + "/user", tags=["User Mail"]
)


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
