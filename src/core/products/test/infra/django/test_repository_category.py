import pytest
import pytest_asyncio

from src.core.products.domain.entity import Category
from src.core.products.infra.database.django.repository import DjangoCategoryRepository
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.database.django.models import Store as StoreModel
from src.core.store.infra.database.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository


@pytest_asyncio.fixture
async def store():
    # Criação do usuário
    user = await DjangoUserRepository().save(
        User(
            email="teste1201@teste.com",
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
            name="Teste 1200",
            slug="teste-1200",
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


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class TestDjangoCategoryRepository:
    @pytest.mark.asyncio
    async def test_create_category(self, store: StoreModel):
        repository = DjangoCategoryRepository()
        category = Category(name="Test Category", store_id=str(store.id))
        created_category = await repository.create(category)
        assert created_category.id is not None
        assert created_category.name == "Test Category"

    @pytest.mark.asyncio
    async def test_list_categories(self, store: StoreModel):
        repository = DjangoCategoryRepository()
        category = Category(name="Test Category", store_id=str(store.id))
        created_category = await repository.create(category)
        categories = await repository.list(store_id=str(created_category.store_id))
        assert len(categories) == 1
        assert categories[0].id == created_category.id
