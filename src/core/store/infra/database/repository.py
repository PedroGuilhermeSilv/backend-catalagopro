from abc import ABC, abstractmethod

from src.core.store.domain.dtos import StoreListDto
from src.core.store.domain.entity import Store


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

    @abstractmethod
    async def list(self) -> list[StoreListDto]:
        pass

    @abstractmethod
    async def update(self, store: Store) -> Store:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass
