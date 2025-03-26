from abc import ABC, abstractmethod

from src.core.products.domain.entity import Category, Product, Size


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category:
        pass


class SizeRepository(ABC):
    @abstractmethod
    def create(self, size: Size) -> Size:
        pass
