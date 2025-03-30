import uuid
from datetime import UTC, datetime

import pytest

from src.core.products.domain.entity import (
    Category,
    Image,
    Price,
    Product,
    Size,
    SizePrice,
)
from src.core.store.domain.entity import BusinessHour, Store

DEFAULT_PRICE = 10.0


@pytest.fixture
def store() -> Store:
    return Store(
        name="Loja Teste",
        owner_id=str(uuid.uuid4()),
        logo_url="https://example.com/logo.png",
        description="Descrição da loja",
        address="Rua Teste, 123",
        whatsapp="11999999999",
        business_hours=[
            BusinessHour(
                day=1,
                open_hour="08:00",
                close_hour="18:00",
            ),
        ],
    )


@pytest.fixture
def category(store: Store) -> Category:
    return Category(
        name="Bebidas",
        store_id=str(store.id),
    )


@pytest.fixture
def price() -> Price:
    return Price(value=10.0)


@pytest.fixture
def size(store: Store) -> Size:
    return Size(name="P", store_id=str(store.id))


@pytest.fixture
def image():
    return Image(url="http://example.com/image.jpg")


class TestProduct:
    def test_create_product_with_default_price(
        self,
        category: Category,
        price: Price,
        image: Image,
    ):
        """Deve criar um produto com preço único"""
        product = Product(
            store_id=str(uuid.uuid4()),
            name="Coca-Cola",
            description="Refrigerante",
            default_price=price,
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        assert product.name == "Coca-Cola"
        assert product.default_price.value == DEFAULT_PRICE
        assert product.has_sizes is False

    def test_create_product_with_size_prices(
        self,
        category: Category,
        price: Price,
        size: Size,
        image: Image,
    ):
        """Deve criar um produto com variação de tamanhos"""
        size_price = SizePrice(size=size, price=price)

        product = Product(
            store_id=str(uuid.uuid4()),
            name="Pizza",
            description="Pizza de calabresa",
            size_price=[size_price],
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        assert product.name == "Pizza"
        assert product.has_sizes is True
        assert len(product.size_price) == 1
        assert product.size_price[0].price.value == DEFAULT_PRICE

    def test_get_price_default(self, category, price, image):
        """Deve retornar o preço default quando não houver tamanho especificado"""
        product = Product(
            store_id=str(uuid.uuid4()),
            name="Coca-Cola",
            description="Refrigerante",
            default_price=price,
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        assert product.get_price() == DEFAULT_PRICE

    def test_get_price_by_size(self, category, price, size, image):
        """Deve retornar o preço do tamanho específico"""
        size_price = SizePrice(size=size, price=price)

        product = Product(
            store_id=str(uuid.uuid4()),
            name="Pizza",
            description="Pizza de calabresa",
            size_price=[size_price],
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        assert product.get_price(size_id=size.id) == DEFAULT_PRICE

    def test_get_price_invalid_size(self, category, price, image):
        """Deve lançar erro quando o tamanho não existir"""
        product = Product(
            store_id=str(uuid.uuid4()),
            name="Pizza",
            description="Pizza de calabresa",
            default_price=price,
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        with pytest.raises(
            ValueError,
            match="Preço não encontrado para o tamanho especificado",
        ):
            product.get_price(size_id="tamanho-inexistente")

    def test_product_without_any_price(self, category, image):
        """Deve lançar erro quando produto não tiver nenhum preço definido"""
        with pytest.raises(ValueError, match="O produto deve ter pelo menos um preço"):
            Product(
                store_id=str(uuid.uuid4()),
                name="Produto sem preço",
                description="Descrição",
                category=category,
                image=[image],
                created_at=datetime.now(tz=UTC),
                updated_at=datetime.now(tz=UTC),
            )

    def test_product_with_both_price_types(self, category, price, size, image):
        """Deve permitir produto com preço default e variações de tamanho"""
        size_price = SizePrice(size=size, price=price)

        product = Product(
            store_id=str(uuid.uuid4()),
            name="Produto Híbrido",
            description="Descrição",
            default_price=price,
            size_price=[size_price],
            category=category,
            image=[image],
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

        assert product.default_price.value == DEFAULT_PRICE
        assert product.has_sizes is True
        assert product.get_price() == DEFAULT_PRICE
        assert product.get_price(size_id=size.id) == DEFAULT_PRICE


class TestCategory:
    def test_create_category(self, store: Store):
        """Deve criar uma categoria com os campos corretos"""
        category = Category(name="Bebidas", store_id=str(store.id))

        assert category.name == "Bebidas"


class TestSize:
    def test_create_size(self, store: Store):
        """Deve criar um tamanho com os campos corretos"""
        size = Size(name="P", store_id=str(store.id))
        assert size.name == "P"
        assert isinstance(size.id, str)


class TestPrice:
    def test_create_price(self):
        """Deve criar um preço com os campos corretos"""
        price = Price(value=10.0)

        assert price.value == DEFAULT_PRICE
