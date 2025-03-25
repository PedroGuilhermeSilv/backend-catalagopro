import os

import pytest
import pytest_asyncio
from ninja.testing import TestAsyncClient

from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository
from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_200 = 200
STATUS_CODE_201 = 201
STATUS_CODE_403 = 403


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest_asyncio.fixture
async def user():
    user = User(
        email="testes1@hotmail.com",
        password="12345678",
        name="test",
        role="ADMIN",
        status="ACTIVE",
    )
    user_repository = DjangoUserRepository()
    await user_repository.save(user)
    return user


@pytest.mark.django_db(transaction=True)
class TestControllerLogin:
    @pytest.mark.asyncio
    async def test_login(self, client, user):
        body_login = {
            "email": "testes1@hotmail.com",
            "password": "12345678",
        }

        response = await client.post("/auth/login/", json=body_login)
        assert response.json().get("token") is not None
        assert response.json().get("exp") is not None
        assert response.json().get("refresh_token") is not None
        assert response.status_code == STATUS_CODE_200

    @pytest.mark.asyncio
    async def test_login_with_invalid_email(self, client):
        body = {
            "email": "test@hotmail.com",
            "password": "12345678",
        }

        response = await client.post("/auth/login/", json=body)
        assert response.status_code == STATUS_CODE_403
        response.json().get("message") == "User not found"

    @pytest.mark.asyncio
    async def test_login_with_invalid_password(self, client, user):
        body_login = {
            "email": user.email,
            "password": "123456789",
        }

        response = await client.post("/auth/login/", json=body_login)
        assert response.status_code == STATUS_CODE_403
        response.json().get("message") == "Invalid password"
