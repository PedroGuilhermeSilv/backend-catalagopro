from collections.abc import Generator

import pytest

from core.user.infra.interfaces.repository import UserRepository
from src.core.user.application.service.dto import (
    InputCreateUser,
    InputUpdateUser,
)
from src.core.user.application.service.user_service import UserService
from src.core.user.domain.entity import UserRole
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.utils.enums import Status

STATUS_CONFLICT = 409


@pytest.fixture(scope="function")
def repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository()
    repo.users.clear()
    yield repo


class TestUpdateUser:
    @pytest.mark.asyncio
    async def test_update_user(self, repository: InMemoryUserRepository):
        request = InputCreateUser(
            email="test@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        service = UserService(repository)
        await service.create_user(input=InputCreateUser(**request.model_dump()))

        user = repository.users[0]

        request_update = InputUpdateUser(
            id=str(user.id),
            email=user.email,
            password=user.password,
            name=user.name,
            role=user.role.value,
            status=user.status.value,
        )
        await service.update_user(input=request_update)

        user_updated = repository.users[0]

        assert user_updated.email == request_update.email
        assert user_updated.id == user.id
        assert user_updated.name == request_update.name
        assert user_updated.role.value == request_update.role.value
        assert user_updated.status.value == request_update.status.value
