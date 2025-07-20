from api.config.logging import get_logger
from api.user.models import User

logger = get_logger(__name__)


class UserRepository:
    """Repository for handling user database operations."""

    def __init__(self, session):
        self.session = session

    def create(self, user_data) -> User:

        user = User(email=user_data.email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        logger.info(f"Created user: {user.email}")
        return user
