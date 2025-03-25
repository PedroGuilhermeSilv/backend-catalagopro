from collections.abc import Generator

import pytest

from src.core.shared.enums import Status
from src.core.user.application.service.user_service import UserService
from src.core.user.domain.entity import User, UserRole
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.user.infra.interfaces.repository import UserRepository

STATUS_CONFLICT = 409


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


class TestGetUserById:
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, repository: InMemoryUserRepository):
        user = repository.users[0]
        service = UserService(repository)
        user_output = await service.get_user_by_id(id=str(user.id))

        assert user_output.id == user.id
        assert user_output.email == user.email
        assert user_output.name == user.name
        assert user_output.role.value == user.role.value
        assert user_output.status.value == user.status.value

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: InMemoryUserRepository):
        user = repository.users[0]
        service = UserService(repository)
        user_output = await service.get_user_by_email(email=user.email)

        assert user_output.id == user.id
        assert user_output.email == user.email
        assert user_output.name == user.name
        assert user_output.role.value == user.role.value
        assert user_output.status.value == user.status.value
