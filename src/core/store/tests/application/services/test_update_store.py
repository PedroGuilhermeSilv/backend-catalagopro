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
from src.core.store.application.services.store_service import (
    InputServiceUpdateStore,
    StoreService,
)
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.in_memory.in_memory_store_repository import (
    InMemoryStoreRepository,
)
from src.core.store.infra.interfaces.repository import StoreRepository
from src.core.user.domain.entity import User, UserRole
from src.core.user.infra.in_memory.in_memory_user import InMemoryUserRepository
from src.core.user.infra.interfaces.repository import UserRepository


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
class TestUpdateStore:
    async def test_update_store(
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

        store = await service.update_store(
            input=InputServiceUpdateStore(
                store_id=store_on_db.id,
                name="Loja Teste Atualizada",
            ),
        )
        assert store.id == store_on_db.id
        assert store.name == "Loja Teste Atualizada"
        assert store.slug == store_on_db.slug
        assert store.owner_id == str(user_on_db.id)
        assert store.created_at == store_on_db.created_at
        assert store.address == store_on_db.address
        assert store.whatsapp == store_on_db.whatsapp
        assert store.description == store_on_db.description
        assert store.logo_url == store_on_db.logo_url
        assert store.business_hours == store_on_db.business_hours
