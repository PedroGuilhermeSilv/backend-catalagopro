import uuid
from collections.abc import Generator

import pytest

from core.user.infra.interfaces.repository import UserRepository
from src.core.user.domain.dto import UserInput
from src.core.user.domain.entity import User, UserRole
from src.core.user.domain.exceptions import UserNotFoundError
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.utils.enums import Status


@pytest.fixture(scope="function")
def repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository()
    yield repo
    repo.users.clear()


class TestDeleteUserWithRepository:
    @pytest.mark.asyncio
    async def test_delete_user(self, repository: UserRepository):
        user = User(
            email="testdelete@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        input = UserInput(
            id=user.id,
            email=user.email,
            password=user.password,
            name=user.name,
            role=user.role.value,
            status=user.status.value,
        )
        user_on_db = await repository.save(input)
        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password
        assert user_on_db.status.value == user.status.value
        assert user_on_db.role.value == user.role.value

        await repository.delete(str(user_on_db.id))
        user_on_db = await repository.get_by_email(user_on_db.email)
        assert user_on_db is None

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, repository: UserRepository):
        with pytest.raises(UserNotFoundError):
            await repository.delete(uuid.uuid4())
