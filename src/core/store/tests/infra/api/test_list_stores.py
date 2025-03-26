import os

import pytest
import pytest_asyncio
from django.test import override_settings
from ninja.testing import TestAsyncClient
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository
from src.framework.urls import api

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

STATUS_CODE_200 = 200
STATUS_CODE_401 = 401


@pytest_asyncio.fixture
async def create_store(client, debug_settings):
    # Criação do usuário
    user = await DjangoUserRepository().save(
        User(
            email="teste@teste.com",
            password="12345678",
            name="Teste",
            role="ADMIN",
            status="ACTIVE",
        ),
    )

    # Criação da loja
    use_case = CreateStoreUseCase(DjangoStoreRepository())
    store = await use_case.execute(
        Store(
            name="Teste",
            slug="teste",
            owner_id=str(user.id),
            status="ACTIVE",
            address="Rua Teste",
            logo_url="https://www.google.com",
            description="Teste",
            whatsapp="1234567890",
            business_hours=[
                BusinessHour(
                    day=DayOfWeek.MONDAY,
                    open_hour="09:00",
                    close_hour="18:00",
                ),
            ],
        ),
    )

    yield store


@pytest.fixture
def client():
    return TestAsyncClient(api)


@pytest.fixture
def debug_settings():
    with override_settings(DEBUG=True):
        yield


@pytest.mark.django_db(transaction=True)
class TestControllerListStores:
    @pytest.mark.asyncio
    async def test_list_stores_empty(self, client, debug_settings):
        headers = {"Authorization": "Bearer " + "1234567890"}
        response = await client.get("/store/", headers=headers)
        assert response.status_code == STATUS_CODE_200

        response_json = response.json()
        assert len(response_json["data"]) == 0  # type: ignore

    @pytest.mark.asyncio
    async def test_list_stores(self, client, debug_settings, create_store: Store):
        headers = {"Authorization": "Bearer " + "1234567890"}
        response = await client.get("/store/", headers=headers)
        assert response.status_code == STATUS_CODE_200

        response_json = response.json()
        assert len(response_json["data"]) == 1  # type: ignore
        assert response_json == {
            "data": [
                {
                    "id": str(create_store.id),
                    "name": create_store.name,
                    "slug": create_store.slug,
                    "created_at": create_store.created_at.strftime("%Y-%m-%d"),
                    "updated_at": create_store.updated_at.strftime("%Y-%m-%d"),
                    "status": create_store.status.value,
                    "logo_url": create_store.logo_url,
                    "description": create_store.description,
                    "address": create_store.address,
                    "whatsapp": create_store.whatsapp,
                    "business_hours": [
                        {
                            "day": create_store.business_hours[0].day.value,
                            "open_hour": create_store.business_hours[
                                0
                            ].formatted_open_hour,
                            "close_hour": create_store.business_hours[
                                0
                            ].formatted_close_hour,
                        },
                    ],
                    "owner_id": create_store.owner_id,
                    "owner_name": "Teste",
                },
            ],
        }
