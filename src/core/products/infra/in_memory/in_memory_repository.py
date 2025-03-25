from src.core.products.domain.entity import Product
from src.core.products.infra.repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products = []

    def create(self, product: Product) -> Product:
        self.products.append(product)
        return product
