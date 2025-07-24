from api.config.logging import get_logger
from api.user.models import User
from api.user.repository import UserRepository
from api.user.schemas import UserBase, UserResponse

logger = get_logger(__name__)


class UserService:
    def __init__(self, session):
        self.session = session
        self.repository = UserRepository(session)

    def create_user(self, user_data: UserBase) -> User:
        return self.repository.create(user_data)

    def get_all_users(self) -> list[UserResponse]:
        users = self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user)

    def delete_user_by_id(self, user_id: str) -> None:
        self.repository.delete_user_by_id(user_id)
