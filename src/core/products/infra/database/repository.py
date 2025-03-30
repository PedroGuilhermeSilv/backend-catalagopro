from abc import ABC, abstractmethod

from src.core.products.domain.entity import Category, Product, Size


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def list(self, store_id: str) -> list[Category]:
        pass


class SizeRepository(ABC):
    @abstractmethod
    async def create(self, size: Size) -> Size:
        pass

    @abstractmethod
    async def list(self, store_id: str) -> list[Size]:
        pass
