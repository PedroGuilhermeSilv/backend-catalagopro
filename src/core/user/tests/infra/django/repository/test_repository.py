import uuid

import pytest
from src.core.user.infra.django.user.repositories.user_repository import (
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
        input = UserInput(
            id=uuid.uuid4(),
            email="test@hotmail.com",
            password="12345678",
        )

        user = await repo.save(user=input)

        assert input.email == user.email
        assert input.id == user.id
        assert input.password != user.password

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, repository: DjangoUserRepository):
        repo = await anext(repository)
        input = UserInput(
            id=uuid.uuid4(),
            email="test@hotmail.com",
            password="12345678",
        )

        await repo.save(user=input)

        user = await repo.get_by_email(email=input.email)

        assert input.email == user.email
        assert input.id == user.id
        assert input.password != user.password
