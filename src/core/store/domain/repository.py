from abc import ABC, abstractmethod
from ast import Store


class StoreRepository(ABC):
    @abstractmethod
    async def save(self, store: Store) -> Store:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Store:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Store:
        pass
