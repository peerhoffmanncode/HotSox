import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..database import schemas

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        active: str = payload.get("active", False)
        superuser: str = payload.get("superuser", False)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(
            username=username, active=bool(active), superuser=bool(superuser)
        )
        return token_data
    except JWTError:
        raise credentials_exception
