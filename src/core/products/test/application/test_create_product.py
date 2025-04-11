import io

import pytest
import pytest_asyncio
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from PIL import Image

from src.core.products.application.services.dto import (
    ProductInputDto,
    SizePriceInputDto,
)
from src.core.products.application.services.service_product import ServiceProduct
from src.core.products.domain.entity import Category, Size
from src.core.products.infra.database.django.repository import (
    DjangoCategoryRepository,
    DjangoProductRepository,
    DjangoSizePriceRepository,
    DjangoSizeRepository,
)
from src.core.products.infra.database.repository import (
    CategoryRepository,
    ProductRepository,
    SizePriceRepository,
    SizeRepository,
)
from src.core.shared.enums import Status
from src.core.shared.file import UploadedFile
from src.core.storage.infra.interfaces.repository import StorageRepository
from src.core.storage.infra.tebi_io.tebi_io_repository import TebiIOStorageRepository
from src.core.store.infra.database.django.models import Store as StoreModel
from src.core.store.infra.database.django.repository import DjangoStoreRepository
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


@pytest_asyncio.fixture
async def product_repository():
    return DjangoProductRepository()


@pytest_asyncio.fixture
async def size_repository():
    return DjangoSizeRepository()


@pytest_asyncio.fixture
async def price_size_repository():
    return DjangoSizePriceRepository()


@pytest_asyncio.fixture
async def storage_repository():
    return TebiIOStorageRepository()


@pytest.mark.asyncio
class TestCreateProduct:
    async def test_create_product(
        self,
        store: StoreModel,
        category_repository: CategoryRepository,
        store_repository: StoreRepository,
        product_repository: ProductRepository,
        size_repository: SizeRepository,
        price_size_repository: SizePriceRepository,
        storage_repository: StorageRepository,
    ):
        service_product = ServiceProduct(
            product_repository=product_repository,
            category_repository=category_repository,
            store_repository=store_repository,
            size_repository=size_repository,
            price_size_repository=price_size_repository,
            storage_repository=storage_repository,
        )
        category = await category_repository.create(
            Category(
                name="Test Category",
                store_id=str(store.id),
            ),
        )

        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, "PNG")
        image_io.seek(0)
        image_bytes = image_io.getvalue()

        test_file = SimpleUploadedFile(
            name="image.png",
            content=image_bytes,
            content_type="image/png",
        )
        test_file.seek(0)
        product_input = ProductInputDto(
            name="Test Product",
            description="Test Description",
            category_id=category.id,
            default_price=10.0,
            image=[
                UploadedFile(
                    name="Test Image",
                    content=image_bytes,
                    content_type="image/png",
                ),
            ],
        )
        product_output = await service_product.create_product(product_input)
        assert product_output.id is not None
        assert product_output.name == "Test Product"
        assert product_output.description == "Test Description"
        assert product_output.category is not None
        assert product_output.category.id == category.id
        assert product_output.category.name == category.name
        assert product_output.category.store_id == category.store_id
        assert product_output.image is not None
        assert len(product_output.image) == 1
        assert product_output.default_price is not None
        assert product_output.default_price.value == 10.0
        assert product_output.size_price is None
        assert product_output.store_id == str(store.id)
        assert product_output.created_at is not None
        assert product_output.updated_at is not None

    async def test_create_product_with_sizes(
        self,
        store: StoreModel,
        category_repository: CategoryRepository,
        store_repository: StoreRepository,
        product_repository: ProductRepository,
        size_repository: SizeRepository,
        price_size_repository: SizePriceRepository,
        storage_repository: StorageRepository,
    ):
        service_product = ServiceProduct(
            product_repository=product_repository,
            category_repository=category_repository,
            store_repository=store_repository,
            size_repository=size_repository,
            price_size_repository=price_size_repository,
            storage_repository=storage_repository,
        )
        category = await category_repository.create(
            Category(
                name="Test Category",
                store_id=str(store.id),
            ),
        )

        image = Image.new("RGB", (100, 100), color="red")
        image_io = io.BytesIO()
        image.save(image_io, "PNG")
        image_io.seek(0)
        image_bytes = image_io.getvalue()

        test_file = SimpleUploadedFile(
            name="image.png",
            content=image_bytes,
            content_type="image/png",
        )
        test_file.seek(0)
        size = await size_repository.create(
            Size(
                name="Test Size",
                store_id=str(store.id),
            ),
        )
        product_input = ProductInputDto(
            name="Test Product",
            description="Test Description",
            category_id=category.id,
            sizes=[
                SizePriceInputDto(
                    size_id=size.id,
                    price=10.0,
                ),
            ],
            image=[
                UploadedFile(
                    name="Test Image",
                    content=image_bytes,
                    content_type="image/png",
                ),
            ],
        )
        product_output = await service_product.create_product(product_input)
        assert product_output.id is not None
        assert product_output.name == "Test Product"
        assert product_output.description == "Test Description"
        assert product_output.size_price is not None
        assert len(product_output.size_price) == 1
        assert product_output.size_price[0].size.id == size.id
        assert product_output.size_price[0].price.value == 10.0
