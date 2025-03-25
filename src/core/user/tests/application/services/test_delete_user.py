from collections.abc import Generator

import pytest

from src.core.shared.enums import Status
from src.core.user.application.service.dto import InputDeleteUser
from src.core.user.application.service.user_service import UserService
from src.core.user.domain.entity import User, UserRole
from src.core.user.domain.exceptions import UserNotFoundError
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


class TestDeleteUser:
    @pytest.mark.asyncio
    async def test_delete_user(self, repository: InMemoryUserRepository):
        user = repository.users[0]
        service = UserService(repository)
        await service.delete_user(
            input=InputDeleteUser(
                id=str(user.id),
            ),
        )

        assert repository.users == []

    @pytest.mark.asyncio
    async def test_raise_exception_when_no_user_found(
        self,
        repository: InMemoryUserRepository,
    ):
        request = InputDeleteUser(
            id="12345678",
        )
        service = UserService(repository)
        with pytest.raises(UserNotFoundError):
            await service.delete_user(input=request)
