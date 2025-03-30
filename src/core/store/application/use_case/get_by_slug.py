from src.core.store.domain.entity import Store

from core.store.infra.database.repository import StoreRepository


class GetStoreBySlugUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def execute(self, slug: str) -> Store:
        try:
            return await self.store_repository.get_by_slug(slug)
        except Exception as e:
            raise e
