import pytest

from src.core.user.domain.entity import User
from core.user.infra.database.repository import (
    DjangoUserRepository,
    UserInput,
)


@pytest.fixture
async def repository():
    repo = DjangoUserRepository()
    await repo.model.objects.all().adelete()
    yield repo


@pytest.mark.django_db
class TestCreateUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, repository: DjangoUserRepository):
        repo = await anext(repository)
        user = User(
            email="test@hotmail.com",
            password="12345678",
        )
        input = UserInput(
            id=user.id,
            email=user.email,
            password=user.password,
        )

        user_on_db = await repo.save(user=input)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: DjangoUserRepository):
        repo = await anext(repository)
        user = User(
            email="test@hotmail.com",
            password="12345678",
        )
        input = UserInput(
            id=user.id,
            email=user.email,
            password=user.password,
        )

        await repo.save(user=input)

        user_on_db = await repo.get_by_email(email=input.email)

        assert user_on_db.email == user.email
        assert user_on_db.id == user.id
        assert user_on_db.password == user.password
