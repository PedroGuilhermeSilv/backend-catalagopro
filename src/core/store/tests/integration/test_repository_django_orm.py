import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from src.core.store.domain.entity import BusinessHour, Store
from src.core.store.infra.database.models import (
    Store as StoreModel,
)
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.user.domain.entity import User, UserRole
from src.core.user.infra.database.models import User as UserModel
from src.core.utils.date import DayOfWeek
from src.core.utils.enums import Status

pytestmark = pytest.mark.django_db  # Marca todos os testes para usar o banco de dados


@pytest.fixture
def user() -> User:
    user_model = UserModel(
        id=str(uuid.uuid4()),
        email="test@hotmail.com",
        password="12345678",
        name="test",
        role=UserRole.ADMIN.value,
        status=Status.ACTIVE.value,
    )
    user_model.save()
    return User(
        id=user_model.id,
        email=user_model.email,
        password=user_model.password,
        name=user_model.name,
        role=user_model.role,
        status=user_model.status,
    )


@pytest.fixture
def store(user: User) -> Store:
    business_hour = BusinessHour(
        day=DayOfWeek.MONDAY,
        open_hour="08:00",
        close_hour="18:00",
    )
    return Store(
        id=str(uuid.uuid4()),
        name="Loja Teste",
        slug="loja-teste",
        owner_id=str(user.id),
        created_at=datetime.now(tz=ZoneInfo("UTC")).date(),
        updated_at=datetime.now(tz=ZoneInfo("UTC")).date(),
        address="Rua Teste, 123",
        whatsapp="1234567890",
        description="Descrição da loja",
        logo_url="https://example.com/logo.png",
        business_hours=[business_hour],
    )


@pytest.mark.django_db(transaction=True)
class TestDjangoStoreRepository:
    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
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

    @pytest.mark.asyncio
    async def test_get_store_not_found(self):
        """Deve lançar exceção quando a loja não for encontrada"""
        # Arrange
        repository = DjangoStoreRepository()

        # Act & Assert
        with pytest.raises(StoreModel.DoesNotExist):
            await repository.get_by_id(str(uuid.uuid4()))

    @pytest.mark.asyncio
    async def test_save_store_with_multiple_hours(self, store: Store):
        business_hours = BusinessHour(
            day=DayOfWeek.SATURDAY,
            open_hour="08:00",
            close_hour="18:00",
        )
        store.business_hours.append(business_hours)

        repository = DjangoStoreRepository()
        saved_store = await repository.save(store)
        expected_business_hours = 2
        assert len(saved_store.business_hours) == expected_business_hours

    @pytest.mark.asyncio
    async def test_list_stores(self, store: Store):
        """Deve listar todas as lojas"""
        repository = DjangoStoreRepository()
        await repository.save(store)

        stores = await repository.list()
        assert len(stores) == 1
        assert stores[0].id == store.id
        assert stores[0].name == store.name
        assert stores[0].slug == store.slug
        assert stores[0].business_hours == store.business_hours
        assert stores[0].created_at == store.created_at
        assert stores[0].updated_at == store.updated_at
