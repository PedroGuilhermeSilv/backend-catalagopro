from abc import ABC, abstractmethod

from src.core.products.domain.entity import Category, Product, Size, SizePrice


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass


class CategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Category:
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


class SizePriceRepository(ABC):
    @abstractmethod
    async def create(self, size_price: SizePrice) -> SizePrice:
        pass
