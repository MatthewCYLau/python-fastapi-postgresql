from sqlalchemy import select, delete
from api.config.exception import AlreadyExistsException, NotFoundException
from api.config.logging import get_logger
from api.config.security import get_password_hash
from api.user.models import User

logger = get_logger(__name__)


class UserRepository:
    """Repository for handling user database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, user_data) -> User:

        existing_user = self.get_by_email(user_data.email)
        if existing_user:
            raise AlreadyExistsException("Email already registered")

        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            date_of_birth=user_data.dateOfBirth,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        logger.info(f"Created user: {user.email}")
        return user

    def get_by_id(self, user_id: str) -> User | None:
        query = select(User).where(User.id == user_id)
        result = self.session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_all(self) -> list[User]:
        query = select(User)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def delete_user_by_id(self, user_id: str) -> None:

        query = delete(User).where(User.id == user_id)
        result = self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"User with id {user_id} not found")

        self.session.commit()
        logger.info(f"Deleted user with id {user_id}")
