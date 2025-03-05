import uuid
from datetime import datetime
import pytest
from django.utils import timezone

from src.core.utils.date import DayOfWeek
from src.core.store.domain.entity import Store, BusinessHour
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.store.infra.database.models import (
    Store as StoreModel,
)

pytestmark = pytest.mark.django_db  # Marca todos os testes para usar o banco de dados


@pytest.fixture
def store() -> Store:
    business_hour = BusinessHour(
        day=DayOfWeek.MONDAY,
        open_hour="08:00",
        close_hour="18:00",
    )
    store = Store(
        id=str(uuid.uuid4()),
        name="Loja Teste",
        slug="loja-teste",
        owner_id=str(uuid.uuid4()),
        created_at=datetime.now().date(),
        updated_at=datetime.now().date(),
        address="Rua Teste, 123",
        whatsapp="1234567890",
        description="Descrição da loja",
        logo_url="https://example.com/logo.png",
        business_hours=[business_hour],
    )
    return store


@pytest.mark.asyncio
class TestDjangoStoreRepository:
    async def test_save_store(self, store: Store):
        """Deve salvar uma loja com seus horários"""
        repository = DjangoStoreRepository()

        saved_store = await repository.save(store)

        assert saved_store.id == store.id
        assert saved_store.name == store.name
        assert saved_store.slug == store.slug
        assert saved_store.business_hours == store.business_hours
        assert saved_store.created_at == store.created_at
        assert saved_store.updated_at == store.updated_at
        assert saved_store.address == store.address
        assert saved_store.whatsapp == store.whatsapp
        assert saved_store.description == store.description
        assert saved_store.logo_url == store.logo_url
        assert saved_store.owner_id == store.owner_id

    async def test_get_store_by_id(self, store: Store):
        """Deve buscar uma loja pelo ID"""
        # Arrange
        repository = DjangoStoreRepository()
        await repository.save(store)

        # Act
        found_store = await repository.get_by_id(str(store.id))

        # Assert
        assert found_store.id == store.id
        assert found_store.name == store.name
        assert found_store.business_hours == store.business_hours

    async def test_get_store_by_slug(self, store: Store):
        """Deve buscar uma loja pelo slug"""
        # Arrange
        repository = DjangoStoreRepository()
        await repository.save(store)

        # Act
        found_store = await repository.get_by_slug(store.slug)

        # Assert
        assert found_store.id == store.id
        assert found_store.slug == store.slug
        assert found_store.business_hours == store.business_hours

    async def test_get_store_not_found(self):
        """Deve lançar exceção quando a loja não for encontrada"""
        # Arrange
        repository = DjangoStoreRepository()

        # Act & Assert
        with pytest.raises(StoreModel.DoesNotExist):
            await repository.get_by_id(str(uuid.uuid4()))

    async def test_save_store_with_multiple_hours(self, store: Store):
        business_hours = BusinessHour(
            day=DayOfWeek.SATURDAY,
            open_hour="08:00",
            close_hour="18:00",
        )
        store.business_hours.append(business_hours)

        repository = DjangoStoreRepository()
        saved_store = await repository.save(store)
        assert len(saved_store.business_hours) == 2
