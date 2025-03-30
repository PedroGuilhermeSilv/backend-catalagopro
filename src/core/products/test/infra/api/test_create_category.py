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
STATUS_CODE_401 = 401


@pytest_asyncio.fixture
async def user(transactional_db) -> UserModel:
    return await UserModel.objects.acreate(
        email="test1@test.com",
        password="test",
    )


@pytest_asyncio.fixture
async def store(transactional_db, user: UserModel):
    return await StoreModel.objects.acreate(
        name="Test Store 9",
        slug="test-store-9",
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


@pytest.mark.django_db(transaction=True)
class TestControllerCreateCategory:
    @pytest.mark.django_db
    def test_create_category_sync(self, debug_settings, store: StoreModel):
        client = Client()
        url = "/api/category/"

        # Convert the data to JSON string and send as content_type='application/json'
        body = {"name": "Prato", "store_slug": store.slug}

        response = client.post(
            url,
            data=json.dumps(body),
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer 1234567890",
        )

        assert response.status_code == STATUS_CODE_201

        response_json = response.json()
        assert response_json["name"] == "Prato"
        assert response_json["store_id"] == str(store.id)
