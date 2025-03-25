from abc import ABC, abstractmethod

from src.core.products.domain.entity import Product


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass
