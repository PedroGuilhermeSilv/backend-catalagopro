from src.core.products.domain.entity import Size
from src.core.products.infra.database.repository import SizeRepository


class ListSizesUseCase:
    def __init__(self, size_repository: SizeRepository):
        self.size_repository = size_repository

    async def execute(self, store_id: str) -> list[Size]:
        return await self.size_repository.list(store_id)
