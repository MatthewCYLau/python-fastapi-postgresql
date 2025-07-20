from sqlalchemy import select
from api.config.logging import get_logger
from api.user.models import User

logger = get_logger(__name__)


class UserRepository:
    """Repository for handling user database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, user_data) -> User:

        existing_user = self.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        user = User(email=user_data.email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        logger.info(f"Created user: {user.email}")
        return user

    def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_all(self) -> list[User]:
        query = select(User)
        result = self.session.execute(query)
        return list(result.scalars().all())
