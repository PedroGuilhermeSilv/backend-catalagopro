from src.core.store.domain.dtos import StoreListDto

from core.store.infra.interfaces.repository import StoreRepository


class ListStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def execute(self) -> list[StoreListDto]:
        try:
            return await self.store_repository.list()
        except Exception as e:
            raise e
