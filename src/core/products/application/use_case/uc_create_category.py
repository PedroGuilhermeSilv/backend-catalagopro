from src.core.products.domain.entity import Category
from src.core.products.infra.database.repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def execute(self, category: Category) -> Category:
        return await self.category_repository.create(category)
