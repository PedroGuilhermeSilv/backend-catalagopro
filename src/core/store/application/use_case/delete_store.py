from core.store.infra.database.repository import StoreRepository


class DeleteStoreUseCase:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    async def execute(self, store_id: str) -> None:
        try:
            await self.store_repository.delete(store_id)
        except Exception as e:
            raise e
