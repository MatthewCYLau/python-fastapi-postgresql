import os
from datetime import timedelta
from api.auth.schemas import LoginData, Token
from api.config.exception import UnauthorizedException
from api.config.logging import get_logger
from api.config.security import create_access_token, verify_password
from api.user.models import User
from api.user.repository import UserRepository
from api.user.schemas import UserCreate, UserResponse, UserUpdate

logger = get_logger(__name__)


class UserService:
    def __init__(self, session):
        self.session = session
        self.repository = UserRepository(session)

    def create_user(self, user_data: UserCreate) -> User:
        return self.repository.create(user_data)

    def get_all_users(self) -> list[UserResponse]:
        users = self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user)

    def delete_user_by_id(self, user_id: str) -> None:
        self.repository.delete_user_by_id(user_id)

    def authenticate(self, login_data: LoginData) -> Token:
        """Authenticate user and return token."""
        user = self.repository.get_by_email(login_data.email)

        if not user or not verify_password(
            login_data.password, str(user.hashed_password)
        ):
            raise UnauthorizedException(detail="Incorrect email or password")

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(
                minutes=os.environ.get("JWT_EXPIRATION_MINUTES", 15)
            ),
        )

        logger.info(f"User authenticated: {user.email}")
        return Token(access_token=access_token)

    def update_user_by_id(self, user_id: str, user_data: UserUpdate) -> User:
        return self.repository.update_by_id(user_id, user_data)
