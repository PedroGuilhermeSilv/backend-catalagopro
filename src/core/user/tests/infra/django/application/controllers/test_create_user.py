import os

import pytest
from ninja.testing import TestAsyncClient

from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_201 = 201
STATUS_CODE_409 = 409
STATUS_CODE_400 = 400


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.mark.django_db(transaction=True)
class TestControllerCreateUser:
    @pytest.mark.asyncio
    async def test_create_user(self, client):
        body = {
            "email": "testes@hotmail.com",
            "password": "12345678",
        }

        response = await client.post("/user/", json=body)
        assert response.json().get("email") == "testes@hotmail.com"
        assert response.status_code == STATUS_CODE_201

    @pytest.mark.asyncio
    async def test_create_user_already_exist(self):
        body = {
            "email": "testes@hotmail.com",
            "password": "12345678",
        }
        client = TestAsyncClient(api)
        response = await client.post("/user/", json=body)
        assert response.status_code == STATUS_CODE_201

        response = await client.post("/user/", json=body)
        assert response.status_code == STATUS_CODE_409
        assert response.json().get("message") == "User already exists"

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self):
        body = {
            "email": "testes",
            "password": "12345678",
        }
        client = TestAsyncClient(api)
        response = await client.post("/user/", json=body)
        assert response.status_code == STATUS_CODE_400
        assert response.json().get("message") == "Invalid email"
