from src.core.products.domain.entity import Product
from src.core.products.infra.database.repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(self, product: Product) -> Product:
        return await self.product_repository.create(product)
