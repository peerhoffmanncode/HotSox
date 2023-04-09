from fastapi import Depends, HTTPException, status, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from . import token
from ..database.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
)


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return token.verify_token(data, credentials_exception)


def check_active(payload: TokenData = Depends(get_current_user)):
    active = payload.active
    if not active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please activate your account first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return payload


def check_superuser(payload: TokenData = Depends(check_active)):
    superuser = payload.superuser
    if not superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: You do not have sufficient permissions to access this endpoint",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return payload
