import os

import pytest
from ninja.testing import TestAsyncClient

from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_200 = 200
STATUS_CODE_201 = 201
STATUS_CODE_403 = 403


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.mark.django_db(transaction=True)
class TestControllerLogin:
    @pytest.mark.asyncio
    async def test_login(self, client):
        body = {
            "email": "testes1@hotmail.com",
            "password": "12345678",
        }

        response = await client.post("/user/", json=body)
        assert response.json().get("email") == "testes1@hotmail.com"
        assert response.status_code == STATUS_CODE_201

        response = await client.post("/auth/login/", json=body)
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
    async def test_login_with_invalid_password(self, client):
        body = {
            "email": "test123@hotmail.com",
            "password": "12345678",
        }

        response = await client.post("/user/", json=body)
        assert response.json().get("email") == "test123@hotmail.com"
        assert response.status_code == STATUS_CODE_201

        body = {
            "email": "test123@hotmail.com",
            "password": "123456789",
        }

        response = await client.post("/auth/login/", json=body)
        assert response.status_code == STATUS_CODE_403
        response.json().get("message") == "Invalid password"
