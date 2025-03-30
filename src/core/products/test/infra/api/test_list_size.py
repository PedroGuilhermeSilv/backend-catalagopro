import json
import os

import pytest
import pytest_asyncio
from django.test import Client, override_settings
from django.utils import timezone

from src.core.shared.enums import Status
from src.core.store.infra.database.django.models import Store as StoreModel
from src.core.user.infra.database.models import User as UserModel

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_201 = 201
STATUS_CODE_200 = 200


@pytest_asyncio.fixture
async def user(transactional_db):
    return await UserModel.objects.acreate(
        email="test82@test.com",
        password="test",
    )


@pytest_asyncio.fixture
async def store(transactional_db, user):
    return await StoreModel.objects.acreate(
        name="Test Store 22",
        slug="test-store-22",
        owner_id=user,
        logo_url="https://test.com/logo.png",
        description="Test Description",
        address="Test Address",
        whatsapp="1234567890",
        business_hours=[
            {
                "day": 1,
                "open_hour": "08:00",
                "close_hour": "18:00",
            },
        ],
        status=Status.ACTIVE.value,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db
class TestListSize:
    def test_list_size(self, debug_settings, store: StoreModel):
        client = Client()
        body = {"name": "Test Size", "store_slug": store.slug}
        response = client.post(
            "/api/size/",
            data=json.dumps(body),
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer 1234567890",
        )
        assert response.status_code == STATUS_CODE_201
        assert response.json()["name"] == "Test Size"
        assert response.json()["store_id"] == str(store.id)

        response = client.get(
            f"/api/size/{store.slug}",
            HTTP_AUTHORIZATION="Bearer 1234567890",
        )
        assert response.status_code == STATUS_CODE_200
        assert response.json()["data"][0]["name"] == "Test Size"
        assert response.json()["data"][0]["store_id"] == str(store.id)
