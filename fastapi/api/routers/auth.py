from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import models, schemas, setup
from fastapi import HTTPException, status
from ..authentication.hashing import Hash
from ..authentication.token import create_access_token

import os

router = APIRouter(prefix=os.environ.get("API_URL", "/api"), tags=["Authentication"])


@router.post("/token")
async def token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(setup.get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == request.username).first()
    )
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    claims = {
        "sub": user.username,
        "email": user.email,
        "superuser": user.is_superuser,
        "active": user.is_active,
    }

    access_token = create_access_token(data=claims)
    return {"access_token": access_token, "token_type": "bearer"}
