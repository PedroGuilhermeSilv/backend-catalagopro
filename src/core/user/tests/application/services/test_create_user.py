from collections.abc import Generator

import pytest

from src.core.shared.enums import Status
from src.core.user.application.service.dto import InputCreateUser
from src.core.user.application.use_case.create_user import CreateUser
from src.core.user.domain.entity import UserRole
from src.core.user.domain.exceptions import (
    InvalidUserError,
    UserAlreadyExistError,
)
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.user.infra.interfaces.repository import UserRepository

STATUS_CONFLICT = 409


@pytest.fixture(scope="function")
def repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository()
    repo.users.clear()
    yield repo


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_user(self, repository: InMemoryUserRepository):
        request = InputCreateUser(
            email="test@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        service = CreateUser(repository)
        response = await service.execute(input=InputCreateUser(**request.model_dump()))

        assert response.email == request.email
        assert response.id is not None

    @pytest.mark.asyncio
    async def test_raise_exception_when_no_email(
        self,
        repository: InMemoryUserRepository,
    ):
        request = InputCreateUser(
            email="",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        service = CreateUser(repository)
        with pytest.raises(InvalidUserError) as excinfo:
            await service.execute(input=request)
        assert str(excinfo.value) == "Invalid user"

    @pytest.mark.asyncio
    async def test_raise_exception_when_user_already_exist(
        self,
        repository: InMemoryUserRepository,
    ):
        request = InputCreateUser(
            email="teste@hotmail.com",
            password="12345678",
            name="test",
            role=UserRole.ADMIN.value,
            status=Status.ACTIVE.value,
        )
        service = CreateUser(repository)
        await service.execute(input=request)

        with pytest.raises(UserAlreadyExistError) as excinfo:
            await service.execute(input=request)

        assert str(excinfo.value) == "User already exists"
        assert excinfo.value.status_code == STATUS_CONFLICT
