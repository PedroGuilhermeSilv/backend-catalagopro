import uuid
from datetime import datetime
from core.store.domain.exceptions import InvalidSlugError
from src.core.store.domain.entity import Store, BusinessHour
import pytest


@pytest.fixture
def business_hour() -> BusinessHour:
    return BusinessHour(
        day=1,
        open_hour="08:00",
        close_hour="18:00",
    )


class TestStoreEntity:
    def test_store_creation_with_explicit_slug(self, business_hour: BusinessHour):
        store_id = str(uuid.uuid4())
        store_name = "Minha Loja Teste"
        explicit_slug = "slug-personalizado"

        store = Store(
            id=store_id,
            name=store_name,
            slug=explicit_slug,
            owner_id=str(uuid.uuid4()),
            created_at=datetime.now().date(),
            updated_at=datetime.now().date(),
            address="Rua Teste, 123",
            whatsapp="1234567890",
            description="Descrição da loja",
            logo_url="https://example.com/logo.png",
            business_hours=[business_hour],
        )

        assert store.slug == explicit_slug
        assert store.name == store_name
        assert store.id == store_id

    def test_store_creation_with_automatic_slug_generation(
        self, business_hour: BusinessHour
    ):
        store_id = str(uuid.uuid4())
        store_name = "Minha Loja Teste"
        expected_slug = "minha-loja-teste"

        store = Store(
            id=store_id,
            name=store_name,
            owner_id=str(uuid.uuid4()),
            created_at=datetime.now().date(),
            updated_at=datetime.now().date(),
            address="Rua Teste, 123",
            whatsapp="1234567890",
            description="Descrição da loja",
            logo_url="https://example.com/logo.png",
            business_hours=[business_hour],
        )

        assert store.slug == expected_slug
        assert store.name == store_name
        assert store.id == store_id

    def test_slug_generation_with_special_characters(self, business_hour: BusinessHour):

        store_id = str(uuid.uuid4())
        store_name = "Café & Restaurante"
        expected_slug = "cafe-restaurante"

        store = Store(
            id=store_id,
            name=store_name,
            owner_id=str(uuid.uuid4()),
            created_at=datetime.now().date(),
            updated_at=datetime.now().date(),
            address="Rua Teste, 123",
            whatsapp="1234567890",
            description="Descrição da loja",
            logo_url="https://example.com/logo.png",
            business_hours=[business_hour],
        )

        assert store.slug == expected_slug

    def test_slug_generation_with_multiple_spaces(self, business_hour: BusinessHour):

        store_id = str(uuid.uuid4())
        store_name = "Loja  com  Espaços  Múltiplos"
        expected_slug = "loja-com-espacos-multiplos"

        store = Store(
            id=store_id,
            name=store_name,
            owner_id=str(uuid.uuid4()),
            created_at=datetime.now().date(),
            updated_at=datetime.now().date(),
            address="Rua Teste, 123",
            whatsapp="1234567890",
            description="Descrição da loja",
            logo_url="https://example.com/logo.png",
            business_hours=[business_hour],
        )

        assert store.slug == expected_slug

    def test_raise_exception_when_name_is_empty(self, business_hour: BusinessHour):
        store_id = str(uuid.uuid4())
        store_name = ""

        with pytest.raises(Exception):
            Store(
                id=store_id,
                name=store_name,
                owner_id=str(uuid.uuid4()),
                created_at=datetime.now().date(),
                updated_at=datetime.now().date(),
                address="Rua Teste, 123",
                whatsapp="1234567890",
                description="Descrição da loja",
                logo_url="https://example.com/logo.png",
                business_hours=[business_hour],
            )
