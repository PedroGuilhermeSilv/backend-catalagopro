import uuid
from collections.abc import Generator
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from src.core.shared.enums import Status
from src.core.storage.infra.in_memory.in_memory_storage_repository import (
    InMemoryStorageRepository,
)
from src.core.storage.infra.interfaces.repository import StorageRepository
from src.core.store.application.services.store_service import StoreService
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.database.in_memory.in_memory_store_repository import (
    InMemoryStoreRepository,
)
from src.core.user.domain.entity import User, UserRole
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.user.infra.interfaces.repository import UserRepository

from core.store.infra.database.repository import StoreRepository


@pytest.fixture(scope="function")
def user_repository() -> Generator[UserRepository, None, None]:
    repo = InMemoryUserRepository(
        users=[
            User(
                email="test@hotmail.com",
                password="12345678",
                name="test",
                role=UserRole.ADMIN.value,
                status=Status.ACTIVE.value,
                store_slug="loja-teste",
            ),
        ],
    )
    yield repo


@pytest.fixture
def storage_repository() -> Generator[StorageRepository, None, None]:
    repo = InMemoryStorageRepository()
    yield repo


@pytest.fixture
def store(user_repository: InMemoryUserRepository) -> Store:
    business_hour = BusinessHour(
        day=DayOfWeek.MONDAY,
        open_hour="08:00",
        close_hour="18:00",
    )
    return Store(
        id=str(uuid.uuid4()),
        name="Loja Teste",
        slug="loja-teste",
        owner_id=str(user_repository.users[0].id),
        created_at=datetime.now(tz=ZoneInfo("UTC")).date(),
        updated_at=datetime.now(tz=ZoneInfo("UTC")).date(),
        address="Rua Teste, 123",
        whatsapp="1234567890",
        description="Descrição da loja",
        logo_url="https://example.com/logo.png",
        business_hours=[business_hour],
    )


@pytest.fixture
def store_repository(store: Store) -> Generator[StoreRepository, None, None]:
    repo = InMemoryStoreRepository(stores=[store])
    yield repo


@pytest.mark.asyncio
class TestListStores:
    async def test_list_stores(
        self,
        store_repository: InMemoryStoreRepository,
        user_repository: InMemoryUserRepository,
        storage_repository: InMemoryStorageRepository,
    ):
        service = StoreService(
            store_repository=store_repository,
            user_repository=user_repository,
            storage_repository=storage_repository,
        )
        store_on_db = store_repository.stores[0]
        user_on_db = user_repository.users[0]
        stores = await service.list_stores()
        assert len(stores.data) == 1
        assert stores.data[0].id == store_on_db.id
        assert stores.data[0].name == store_on_db.name
        assert stores.data[0].slug == store_on_db.slug
        assert stores.data[0].owner_id == str(user_on_db.id)
        assert stores.data[0].owner_name == user_on_db.name
