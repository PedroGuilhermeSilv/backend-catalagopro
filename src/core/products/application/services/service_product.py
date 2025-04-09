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
from src.core.products.domain.entity import Price, Product, SizePrice
from src.core.products.infra.database.repository import (
    CategoryRepository,
    ProductRepository,
    SizePriceRepository,
    SizeRepository,
)


class ServiceProduct:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
        size_repository: SizeRepository,
        store_repository: StoreRepository,
        price_size_repository: SizePriceRepository,
    ):
        self.product_repository = product_repository
        self.uc_create_product = CreateProductUseCase(product_repository)
        self.uc_create_size_price = UCCreateSizePrice(price_size_repository)
        self.service_category = CategoryService(category_repository, store_repository)
        self.service_size = SizeService(size_repository, store_repository)

    async def create_product(self, input: ProductInputDto) -> ProductOutputDto:
        category = await self.service_category.get_category_by_id(input.category_id)
        default_price = None
        if input.default_price:
            default_price = Price(value=input.price)
        size_price = []
        if input.sizes:
            for size_price in input.sizes:
                size = await self.service_size.get_size_by_id(size_price.size_id)
                price = await self.uc_create_size_price.execute(
                    SizePrice(
                        size=size,
                        price=Price(value=size_price.price),
                    ),
                )
                size_price.append(price)

        product = Product(
            name=input.name,
            description=input.description,
            category=category,
            store_id=category.store_id,
            default_price=default_price,
            size_price=size_price,
        )
        return await self.uc_create_product.execute(product)
