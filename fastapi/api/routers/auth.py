from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import models, schemas, setup
from fastapi import HTTPException, status
from ..authentication.hashing import Hash
from ..authentication.token import create_access_token

from datetime import datetime, timedelta
import os
import sys
from slowapi.util import get_remote_address
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix=os.environ.get("FASTAPI_URL", "/fastapi/v1"), tags=["Authentication"]
)

if "test" in sys.argv[0] or "test" in sys.argv[1]:
    max_attempts = 250
else:
    max_attempts = 5


@router.post(
    "/token",
    status_code=200,
)
@limiter.limit(f"{max_attempts}/minute")
async def token(
    request: Request,
    body: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(setup.get_db),
):
    user = db.query(models.User).filter(models.User.username == body.username).first()
    if not user or not Hash.verify(user.password, body.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    claims = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "superuser": user.is_superuser,
        "active": user.is_active,
    }

    access_token = create_access_token(claims=claims)
    return {"access_token": access_token, "token_type": "bearer"}
