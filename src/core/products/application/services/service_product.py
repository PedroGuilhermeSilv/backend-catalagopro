from datetime import UTC, datetime

from core.store.infra.database.repository import StoreRepository
from src.core.products.application.services.dto import (
    ProductInputDto,
    ProductOutputDto,
)
from src.core.products.application.services.service_category import CategoryService
from src.core.products.application.services.service_size import SizeService
from src.core.products.application.use_case.uc_create_product import (
    CreateProductUseCase,
)
from src.core.products.application.use_case.uc_create_size_price import (
    UCCreateSizePrice,
)
from src.core.products.domain.entity import (
    Category,
    Image,
    Price,
    Product,
    Size,
    SizePrice,
)
from src.core.products.infra.database.repository import (
    CategoryRepository,
    ProductRepository,
    SizePriceRepository,
    SizeRepository,
)
from src.core.storage.application.use_case.dto import SaveFileInput
from src.core.storage.application.use_case.save_file import SaveFile
from src.core.storage.infra.interfaces.repository import StorageRepository


class ServiceProduct:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        size_repository: SizeRepository,
        store_repository: StoreRepository,
        price_size_repository: SizePriceRepository,
        storage_repository: StorageRepository,
    ):
        self.uc_create_product = CreateProductUseCase(product_repository)
        self.uc_create_size_price = UCCreateSizePrice(price_size_repository)
        self.service_category = CategoryService(category_repository, store_repository)
        self.service_size = SizeService(size_repository, store_repository)
        self.uc_save_file = SaveFile(storage_repository)

    async def create_product(self, input: ProductInputDto) -> ProductOutputDto:
        category = await self.service_category.get_category_by_id(input.category_id)
        default_price = None
        if input.default_price:
            default_price = Price(value=input.default_price)
        size_prices = []
        if input.sizes:
            for size_price in input.sizes:
                size = await self.service_size.get_size_by_id(size_price.size_id)
                price = await self.uc_create_size_price.execute(
                    SizePrice(
                        size=Size(
                            id=size.id,
                            name=size.name,
                            store_id=size.store_id,
                        ),
                        price=Price(value=size_price.price),
                    ),
                )
                size_prices.append(price)

        images = []
        if input.image:
            for image in input.image:
                file_name = f"{image.name}-{datetime.now(UTC).strftime('%Y-%m-%d')}.png"
                image_on_storage = self.uc_save_file.execute(
                    SaveFileInput(
                        file=image,
                    ),
                    file_name=file_name,
                )
                image_created = Image(url=image_on_storage.file_url)
                images.append(image_created)
        product = Product(
            name=input.name,
            description=input.description,
            category=Category(
                id=category.id,
                name=category.name,
                store_id=category.store_id,
            ),
            store_id=category.store_id,
            default_price=default_price,
            size_price=size_prices,
            image=images,
        )
        product_on_db = await self.uc_create_product.execute(product)

        return ProductOutputDto(
            id=product_on_db.id,
            name=product_on_db.name,
            description=product_on_db.description,
            default_price=product_on_db.default_price,
            size_price=product_on_db.size_price,
            category=product_on_db.category,
            image=product_on_db.image,
            created_at=product_on_db.created_at,
            updated_at=product_on_db.updated_at,
            store_id=product_on_db.store_id,
        )
