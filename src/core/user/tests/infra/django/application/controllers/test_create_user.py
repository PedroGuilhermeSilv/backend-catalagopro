import os

import pytest
from django.test import override_settings
from ninja.testing import TestAsyncClient

from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_201 = 201
STATUS_CODE_409 = 409
STATUS_CODE_400 = 400


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db(transaction=True)
class TestControllerCreateUser:
    @pytest.mark.asyncio
    async def test_create_user(self, client, debug_settings):
        headers = {"Authorization": "Bearer " + "1234567890"}
        body = {
            "email": "testes@hotmail.com",
            "password": "12345678",
            "name": "test",
            "role": "ADMIN",
            "status": "ACTIVE",
        }

        response = await client.post("/user/", json=body, headers=headers)
        assert response.json().get("email") == "testes@hotmail.com"
        assert response.status_code == STATUS_CODE_201

    @pytest.mark.asyncio
    async def test_create_user_already_exist(self, client, debug_settings):
        headers = {"Authorization": "Bearer " + "1234567890"}
        body = {
            "email": "testes@hotmail.com",
            "password": "12345678",
            "name": "test",
            "role": "ADMIN",
            "status": "ACTIVE",
        }
        response = await client.post("/user/", json=body, headers=headers)
        assert response.status_code == STATUS_CODE_201

        response = await client.post("/user/", json=body, headers=headers)
        assert response.status_code == STATUS_CODE_409
        assert response.json().get("message") == "User already exists"

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self, client, debug_settings):
        headers = {"Authorization": "Bearer " + "1234567890"}
        body = {
            "email": "testes",
            "password": "12345678",
            "name": "test",
            "role": "ADMIN",
            "status": "ACTIVE",
        }
        response = await client.post("/user/", json=body, headers=headers)
        assert response.status_code == STATUS_CODE_400
        assert response.json().get("message") == "Invalid email"
