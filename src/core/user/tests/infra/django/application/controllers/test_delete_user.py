import os

import pytest
from django.test import override_settings
from ninja.testing import TestAsyncClient

from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_201 = 201
STATUS_CODE_409 = 409
STATUS_CODE_400 = 400
STATUS_CODE_204 = 204


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db(transaction=True)
class TestControllerDeleteUser:
    @pytest.mark.asyncio
    async def test_delete_user(self, client, debug_settings):
        body = {
            "email": "testes@hotmail.com",
            "password": "12345678",
            "name": "test",
            "role": "ADMIN",
            "status": "ACTIVE",
        }
        headers = {"Authorization": "Bearer " + "1234567890"}

        response = await client.post("/user/", json=body, headers=headers)
        assert response.json().get("email") == "testes@hotmail.com"
        assert response.status_code == STATUS_CODE_201

        response = await client.delete(
            f"/user/{response.json().get('id')}",
            headers=headers,
        )
        assert response.status_code == STATUS_CODE_204
