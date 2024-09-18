from src.core.user.domain.dto.user_dto import UserInput, UserOutput
from src.core.user.domain.entity import User
from src.core.user.domain.repository.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self, users: list[User] = []):
        self.users = users

    async def save(self, user: UserInput) -> UserOutput:
        user_ = User(**user.model_dump())
        self.users.append(user_)
        return UserOutput(email=user_.email, id=user_.id, password=user_.password)

    async def get_by_email(self, email: str) -> UserOutput:
        return next(
            (
                UserOutput(email=user.email, id=user.id, password=user.password)
                for user in self.users
                if user.email == email
            ),
            None,
        )

    def clear(self):
        self.users = []
