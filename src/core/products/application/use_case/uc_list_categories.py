from src.core.products.domain.entity import Category
from src.core.products.infra.database.repository import CategoryRepository


class ListCategoriesUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self, store_id: str) -> list[Category]:
        return await self.category_repository.list(store_id)
