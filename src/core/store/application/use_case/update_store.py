from src.core.store.domain.entity import Store

from core.store.infra.interfaces.repository import StoreRepository


class UpdateStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def execute(self, store: Store) -> Store:
        try:
            return await self.store_repository.update(store)
        except Exception as e:
            raise e
