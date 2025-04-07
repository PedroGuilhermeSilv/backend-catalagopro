from uuid import uuid4

import pytest
import pytest_asyncio

from src.core.products.domain.entity import Price, Size, SizePrice
from src.core.products.infra.database.django.repository import (
    DjangoSizePriceRepository,
    DjangoSizeRepository,
)
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour, DayOfWeek
from src.core.store.infra.database.django.repository import DjangoStoreRepository
from src.core.user.domain.entity import User
from src.core.user.infra.database.repository import DjangoUserRepository


@pytest_asyncio.fixture
async def size():
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

    size = await DjangoSizeRepository().create(
        Size(name="Tamanho 1", store_id=store.id),
    )
    yield size


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class TestDjangoSizePriceRepository:
    @pytest.mark.asyncio
    async def test_create(self, size: Size):
        repository = DjangoSizePriceRepository()
        size_price = SizePrice(
            size=size,
            price=Price(id=str(uuid4()), value=10),
        )
        result = await repository.create(size_price)
        assert result.id == size_price.id
        assert result.size.id == size_price.size.id
        assert result.price.id == size_price.price.id
        assert result.price.value == size_price.price.value
