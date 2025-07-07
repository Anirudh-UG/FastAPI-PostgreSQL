from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from pydantic import Secret
import logging
from app import schemas

# generated using the bash command "openssl rand -hex 32"
SECRET_KEY = "603b86a0c7edba0746b5b954fd16f2f72cfcffdf1ae0ea9b624fc6c66a3c483c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRATION_MINUTES
    )
    to_encode.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: Optional[int] = payload.get("user_id")

        if id == None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    except AssertionError as e:
        print(e)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
