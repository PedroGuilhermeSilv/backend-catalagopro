from core.products.infra.database.repository import ProductRepository
from src.core.products.domain.entity import Product


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products = []

    def create(self, product: Product) -> Product:
        self.products.append(product)
        return product
