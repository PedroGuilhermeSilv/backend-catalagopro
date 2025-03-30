import pytest
import pytest_asyncio

from src.core.products.domain.entity import Size
from src.core.products.infra.database.django.repository import DjangoSizeRepository
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.database.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository


@pytest_asyncio.fixture
async def store():
    # Criação do usuário
    user = await DjangoUserRepository().save(
        User(
            email="teste2@teste.com",
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
            name="Teste 123",
            slug="teste-123",
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
class TestDjangoSizeRepository:
    @pytest.mark.asyncio
    async def test_create_size(self, store: Store):
        repository = DjangoSizeRepository()
        size = Size(name="Test Size", store_id=str(store.id))
        created_size = await repository.create(size)
        assert created_size.id is not None
        assert created_size.name == "Test Size"

    @pytest.mark.asyncio
    async def test_list_sizes(self, store: Store):
        repository = DjangoSizeRepository()
        size = Size(name="Test Size", store_id=str(store.id))
        await repository.create(size)
        sizes = await repository.list(str(store.id))
        assert len(sizes) == 1
        assert sizes[0].name == "Test Size"
