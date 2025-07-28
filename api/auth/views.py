from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.auth.schemas import LoginData, Token
from api.config.database import get_session
from api.config.logging import get_logger
from api.config.security import get_current_user
from api.user.schemas import UserResponse
from api.user.service import UserService

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_session),
) -> Token:
    """Authenticate user and return token."""
    login_data = LoginData(email=form_data.username, password=form_data.password)
    logger.info(login_data)
    return UserService(session).authenticate(login_data)


@router.get("/", response_model=UserResponse)
def get_current_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return current_user
