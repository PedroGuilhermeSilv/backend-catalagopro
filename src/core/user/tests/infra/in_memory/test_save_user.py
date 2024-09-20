import uuid
from collections.abc import Generator

import pytest

from src.core.user.domain.dto.user_dto import UserInput
from src.core.user.domain.entity import User
from src.core.user.domain.repository.user_repository import UserRepository
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository


@pytest.fixture(scope="function")
def repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository()
    yield repo
    repo.users.clear()


class TestSaveUserWithRepository:
    @pytest.mark.asyncio
    async def test_save_user(self, repository: UserRepository):
        user = User(
            email="test@hotmail.com",
            password="12345678",
        )
        input = UserInput(
            id=user.id,
            email=user.email,
            password=user.password,
        )
        user_on_db = await repository.save(input)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: UserRepository):
        input = UserInput(
            id=uuid.uuid4(),
            email="teste@hotmail.com",
            password="12345678",
        )
        user = await repository.save(input)

        response = await repository.get_by_email(user.email)

        assert response.email == user.email
        assert response.id == user.id
        assert response.password == user.password
