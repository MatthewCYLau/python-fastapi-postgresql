from fastapi import APIRouter, Depends, status

from api.config.database import get_session
from api.config.logging import get_logger
from api.user.schemas import UserBase
from api.user.service import UserService

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["users"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserBase, session=Depends(get_session)):
    """Register a new user."""
    logger.info(f"Registering user: {user_data.email}")
    return UserService(session).create_user(user_data)
