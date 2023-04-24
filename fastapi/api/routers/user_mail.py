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
from ..controller import ctr_mail

import os
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

# build routes
router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1") + "/user", tags=["User Mail"]
)


##
## Mail
##
@router.get(
    "/mail",
    response_model=Page[schemas.MessageMail_with_id],
    dependencies=[Depends(oauth2.check_active)],
    status_code=200,
)
@limiter.limit("30/minute")
async def get_all_mail(
    request: Request,
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    return paginate(ctr_mail.show_all_mails(current_user.username, db), params)


@router.post(
    "/mail",
    response_model=schemas.MessageMail_with_id,
    dependencies=[Depends(oauth2.check_active)],
    status_code=201,
)
@limiter.limit("20/minute")
async def send_mail(
    request: Request,
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
    status_code=204,
)
@limiter.limit("20/minute")
async def delete_mail(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.ShowUser = Depends(oauth2.get_current_user),
):
    # as long as response is set to 204
    # we do net get a JSON as return :-( !
    return ctr_mail.delete_mail(current_user.username, id, db)
