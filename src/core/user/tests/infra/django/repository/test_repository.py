import uuid

import pytest
import pytest_asyncio

from src.core.shared.enums import Status
from src.core.shared.hash import verify_password
from src.core.user.domain.entity import User, UserRole
from src.core.user.domain.exceptions import UserNotFoundError
from src.core.user.infra.database.repository import (
    DjangoUserRepository,
    UserInput,
)


@pytest_asyncio.fixture
async def repository():
    repo = DjangoUserRepository()
    await repo.model.objects.all().adelete()
    yield repo


@pytest.mark.django_db
class TestGetUserByEmail:
    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: DjangoUserRepository):
        user = User(
            email="test@hotmail.com",
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

        await repository.save(user=input)

        user_on_db = await repository.get_by_email(email=input.email)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password
        assert user_on_db.status.value == user.status.value
        assert user_on_db.role.value == user.role.value


@pytest.mark.django_db
class TestCreateUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, repository: DjangoUserRepository):
        user = User(
            email="test@hotmail.com",
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

        user_on_db = await repository.save(user=input)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.status.value == user.status.value
        assert user_on_db.role.value == user.role.value

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: DjangoUserRepository):
        user = User(
            email="test@hotmail.com",
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

        await repository.save(user=input)

        user_on_db = await repository.get_by_email(email=input.email)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password
        assert user_on_db.status.value == user.status.value
        assert user_on_db.role.value == user.role.value

    @pytest.mark.asyncio
    async def test_list_users(self, repository: DjangoUserRepository):
        users = [
            User(
                email=f"test{i}@hotmail.com",
                password="12345678",
                name=f"test{i}",
                role=UserRole.ADMIN.value,
                status=Status.ACTIVE.value,
            )
            for i in range(3)
        ]

        for user in users:
            input = UserInput(
                id=user.id,
                email=user.email,
                password=user.password,
                name=user.name,
                role=user.role.value,
                status=user.status.value,
            )
            await repository.save(user=input)

        users_from_db = await repository.list()

        expected_users = 3

        assert len(users_from_db) == expected_users

        for i, user_db in enumerate(users_from_db):
            assert user_db.email == f"test{i}@hotmail.com"
            assert user_db.name == f"test{i}"
            assert user_db.role.value == UserRole.ADMIN.value
            assert user_db.status.value == Status.ACTIVE.value


@pytest.mark.django_db
class TestDeleteUserRepository:
    @pytest.mark.asyncio
    async def test_delete_user(self, repository: DjangoUserRepository):
        user = User(
            email="test@hotmail.com",
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

        await repository.save(user=input)

        await repository.delete(user.id)

        user_on_db = await repository.get_by_email(user.email)
        assert user_on_db is None

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, repository: DjangoUserRepository):
        with pytest.raises(UserNotFoundError):
            await repository.delete(uuid.uuid4())


@pytest.mark.django_db
class TestUpdateUserRepository:
    @pytest.mark.asyncio
    async def test_update_user(self, repository: DjangoUserRepository):
        user = User(
            email="test@hotmail.com",
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
        await repository.save(user=input)

        user_updated = User(
            id=user.id,
            email="newemail@hotmail.com",
            name="new name",
            role=UserRole.EMPLOYEE.value,
            status=Status.INACTIVE.value,
            password="87654321",
        )

        input = UserInput(
            id=user_updated.id,
            email=user_updated.email,
            password=user_updated.password,
            name=user_updated.name,
            role=user_updated.role.value,
            status=user_updated.status.value,
        )
        await repository.update(input)
        user_on_db = await repository.get_by_email(input.email)

        assert user_on_db.email == input.email
        assert user_on_db.id == input.id
        assert user_on_db.status.value == input.status.value
        assert user_on_db.role == input.role
        assert verify_password("87654321", user_on_db.password)

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, repository: DjangoUserRepository):
        with pytest.raises(UserNotFoundError):
            await repository.update(
                UserInput(
                    id=uuid.uuid4(),
                    email="test@hotmail.com",
                    password="12345678",
                    name="test",
                    role=UserRole.ADMIN.value,
                    status=Status.ACTIVE.value,
                ),
            )
