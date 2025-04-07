from core.products.infra.database.repository import CategoryRepository
from src.core.products.domain.entity import Category


class UCGetByIdCategory:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self, id: str) -> Category:
        return await self.category_repository.get_by_id(id)
