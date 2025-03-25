from src.core.store.domain.entity import Store
from src.core.store.infra.interfaces.repository import StoreRepository


class GetStoreByIdUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def execute(self, store_id: str) -> Store:
        try:
            return await self.store_repository.get_by_id(store_id)
        except Exception as e:
            raise e
