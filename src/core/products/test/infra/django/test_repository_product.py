import pytest
import pytest_asyncio

from src.core.products.domain.entity import Category, Image, Price, Product, Size
from src.core.products.infra.database.django.repository import (
    DjangoCategoryRepository,
    DjangoProductRepository,
    DjangoSizeRepository,
)
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import BusinessHour, Store
from src.core.store.domain.enums import DayOfWeek
from src.core.store.infra.database.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository


@pytest_asyncio.fixture
async def store():
    # Criação do usuários
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

    yield Store(
        id=str(store.id),
        name=store.name,
        slug=store.slug,
        owner_id=str(store.owner_id),
        status=store.status,
        address=store.address,
        logo_url=store.logo_url,
        description=store.description,
        whatsapp=store.whatsapp,
        business_hours=store.business_hours,
    )


@pytest_asyncio.fixture
async def category(store: Store):
    category = Category(name="Teste", store_id=str(store.id))
    await DjangoCategoryRepository().create(category)
    yield Category(
        id=str(category.id),
        name=category.name,
        store_id=str(category.store_id),
    )


@pytest_asyncio.fixture
async def size(store: Store):
    size = Size(name="Teste", store_id=str(store.id))
    await DjangoSizeRepository().create(size)
    yield Size(
        id=str(size.id),
        name=size.name,
        store_id=str(size.store_id),
    )


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class TestDjangoProductRepository:
    @pytest.mark.asyncio
    async def test_create_product_only_one_price(
        self,
        store: Store,
        category: Category,
        size: Size,
    ):
        product = Product(
            name="Teste",
            store_id=str(store.id),
            description="Teste",
            default_price=Price(value=10.0),
            category=category,
            image=[
                Image(
                    url="https://www.google.com",
                ),
            ],
        )
        product_on_db = await DjangoProductRepository().create(product)
        assert product_on_db.id is not None
        assert product_on_db.name == "Teste"
        assert product_on_db.description == "Teste"
        assert product_on_db.default_price.value == 10.0
        assert product_on_db.category == category
        assert product_on_db.image[0].url == "https://www.google.com"
