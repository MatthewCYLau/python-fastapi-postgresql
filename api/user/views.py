import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.config.database import get_session
from api.config.logging import get_logger
from api.user.schemas import UserCreate, UserResponse
from api.user.service import UserService
from api.user.repository import UserRepository

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    repository = UserRepository(session)
    return UserService(repository)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, session=Depends(get_session)) -> UserResponse:
    """Register a new user."""
    logger.info(f"Registering user: {user_data.email}")
    return UserService(session).create_user(user_data)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    session=Depends(get_session),
) -> list[UserResponse]:
    """Get all users."""
    logger.debug("Fetching all users")
    try:
        users = UserService(session).get_all_users()
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Failed to fetch users: {str(e)}")
        raise


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: uuid.UUID,
    session=Depends(get_session),
) -> UserResponse:
    logger.info(f"Getting user {user_id}")
    try:
        user = UserService(session).get_user_by_id(user_id)
        logger.info(f"Retrieved user {user_id}")
        return user
    except Exception as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        raise


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def create_user(user_id: uuid.UUID, session=Depends(get_session)):
    logger.info(f"Deleting user: {user_id}")
    UserService(session).delete_user_by_id(user_id)
