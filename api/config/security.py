from typing import Annotated
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

import jwt
import os

from pydantic import BaseModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ.get("JWT_SECRET"), algorithm=ALGORITHM
    )
    return encoded_jwt


class TokenData(BaseModel):
    user_id: str | None = None


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.environ.get("JWT_SECRET"), algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.InvalidTokenError:
        raise credentials_exception

    # import here to avoid circular imports
    from api.config.database import get_session  # type: ignore
    from api.user.service import UserService  # type: ignore

    for session in get_session():
        user = UserService(session).get_user_by_id(token_data.user_id)
        if user is None:
            raise credentials_exception
        return user
