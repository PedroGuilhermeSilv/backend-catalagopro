import uuid
from collections.abc import Generator

import pytest

from src.core.shared.enums import Status
from src.core.shared.hash import verify_password
from src.core.user.domain.dto import UserInput
from src.core.user.domain.entity import User, UserRole
from src.core.user.domain.exceptions import UserNotFoundError
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.user.infra.interfaces.repository import UserRepository


@pytest.fixture(scope="function")
def repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository(
        users=[
            User(
                email="test@hotmail.com",
                password="12345678",
                name="test",
                role=UserRole.ADMIN.value,
                status=Status.ACTIVE.value,
            ),
        ],
    )
    yield repo
    repo.users.clear()


class TestUpdateUserWithRepository:
    @pytest.mark.asyncio
    async def test_update_user(self, repository: UserRepository):
        user = repository.users[0]
        input = UserInput(
            id=user.id,
            email="novoemail@hotmail.com",
            password="12345678",
            name="novo nome",
            role=user.role.value,
            status=user.status.value,
        )
        await repository.update(input)
        user_on_db = repository.users[0]
        assert user_on_db.email == input.email
        assert user_on_db.id == input.id
        assert verify_password(input.password, user_on_db.password)
        assert user_on_db.status.value == input.status.value
        assert user_on_db.role.value == input.role.value

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, repository: UserRepository):
        input = UserInput(
            id=uuid.uuid4(),
            email="novoemail@hotmail.com",
            password="12345678",
            name="novo nome",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        with pytest.raises(UserNotFoundError):
            await repository.update(input)
