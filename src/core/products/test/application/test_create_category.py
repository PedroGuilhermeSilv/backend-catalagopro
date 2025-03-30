import pytest
import pytest_asyncio
from django.utils import timezone

from core.products.infra.database.django.repository import (
    DjangoCategoryRepository,
)
from core.shared.enums import Status
from core.store.infra.database.django.repository import DjangoStoreRepository
from src.core.products.application.services.dto import CategoryInputDto
from src.core.products.application.services.service_category import CategoryService
from src.core.products.infra.database.repository import CategoryRepository
from src.core.store.infra.database.django.models import Store as StoreModel
from src.core.store.infra.database.repository import StoreRepository
from src.core.user.infra.database.models import User as UserModel


@pytest_asyncio.fixture
async def user(transactional_db):
    return await UserModel.objects.acreate(
        email="test@test.com",
        password="test",
    )


@pytest_asyncio.fixture
async def store(transactional_db, user):
    return await StoreModel.objects.acreate(
        name="Test Store",
        slug="test-store",
        owner_id=user,
        logo_url="https://test.com/logo.png",
        description="Test Description",
        address="Test Address",
        whatsapp="1234567890",
        business_hours=[
            {
                "day": 1,
                "open_hour": "08:00",
                "close_hour": "18:00",
            },
        ],
        status=Status.ACTIVE.value,
        created_at=timezone.now(),
        updated_at=timezone.now(),
    )


@pytest_asyncio.fixture
async def category_repository():
    return DjangoCategoryRepository()


@pytest_asyncio.fixture
async def store_repository():
    return DjangoStoreRepository()


@pytest.mark.asyncio
class TestCreateCategory:
    async def test_create_category(
        self,
        store: StoreModel,
        category_repository: CategoryRepository,
        store_repository: StoreRepository,
    ):
        category_service = CategoryService(
            category_repository=category_repository,
            store_repository=store_repository,
        )

        category = CategoryInputDto(name="Test Category", store_slug=store.slug)
        category_output = await category_service.create_category(category)

        assert category_output.id is not None
        assert category_output.name == "Test Category"
