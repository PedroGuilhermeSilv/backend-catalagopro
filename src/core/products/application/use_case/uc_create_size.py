from src.core.products.domain.entity import Size
from src.core.products.infra.database.repository import SizeRepository


class CreateSizeUseCase:
    def __init__(self, size_repository: SizeRepository):
        self.size_repository = size_repository

    async def execute(self, size: Size) -> Size:
        return await self.size_repository.create(size)
