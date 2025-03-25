from src.core.user.domain.dto import UserInput, UserOutput
from src.core.user.domain.entity import User
from src.core.user.domain.exceptions import UserNotFoundError
from src.core.user.infra.interfaces.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self, users: list[User] = []):
        self.users = users

    async def save(self, user: UserInput) -> UserOutput:
        self.users.append(user)
        return UserOutput(
            email=user.email,
            id=user.id,
            password=user.password,
            name=user.name,
            role=user.role,
            store_slug=user.store_slug,
            status=user.status,
        )

    async def get_by_email(self, email: str) -> UserOutput:
        return next(
            (
                UserOutput(
                    email=user.email,
                    id=user.id,
                    password=user.password,
                    name=user.name,
                    role=user.role.value,
                    store_slug=user.store_slug,
                    status=user.status.value,
                )
                for user in self.users
                if user.email == email
            ),
            None,
        )

    async def list(self) -> list[UserOutput]:
        return [
            UserOutput(
                email=user.email,
                id=user.id,
                password=user.password,
                name=user.name,
                role=user.role.value,
                store_slug=user.store_slug,
                status=user.status.value,
            )
            for user in self.users
        ]

    async def delete(self, id: str) -> None:
        for i, user in enumerate(self.users):
            if str(user.id) == id:
                self.users.pop(i)
                return
        raise UserNotFoundError

    async def update(self, user: UserInput) -> UserOutput:
        for index, user_on_db in enumerate(self.users):
            if str(user_on_db.id) == str(user.id):
                self.users[index] = User(
                    email=user.email,
                    password=user.password,
                    name=user.name,
                    role=user.role.value,
                    status=user.status.value,
                    id=user.id,
                    store_slug=user.store_slug,
                )
                return UserOutput(
                    email=user.email,
                    id=user.id,
                    password=user.password,
                    name=user.name,
                    role=user.role.value,
                    store_slug=user.store_slug,
                    status=user.status.value,
                )
        raise UserNotFoundError

    async def get_by_id(self, id: str) -> UserOutput | None:
        return next(
            (
                UserOutput(
                    email=user.email,
                    id=user.id,
                    password=user.password,
                    name=user.name,
                    role=user.role.value,
                    store_slug=user.store_slug,
                    status=user.status.value,
                )
                for user in self.users
                if str(user.id) == id
            ),
            None,
        )
