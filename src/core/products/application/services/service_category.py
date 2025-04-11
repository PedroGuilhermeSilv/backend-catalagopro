from src.core.products.application.services.dto import (
    CategoryInputDto,
    CategoryListOutputDto,
    CategoryOutputDto,
)
from src.core.products.application.use_case.uc_create_category import (
    CreateCategoryUseCase,
)
from src.core.products.application.use_case.uc_get_by_id_category import (
    UCGetByIdCategory,
)
from src.core.products.application.use_case.uc_list_categories import (
    ListCategoriesUseCase,
)
from src.core.products.domain.entity import Category
from src.core.products.infra.database.repository import CategoryRepository
from src.core.store.application.use_case.get_by_slug import GetStoreBySlugUseCase
from src.core.store.infra.database.repository import StoreRepository


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        store_repository: StoreRepository,
    ):
        self.category_repository = category_repository
        self.store_repository = store_repository
        self.uc_create_category = CreateCategoryUseCase(self.category_repository)
        self.uc_get_store = GetStoreBySlugUseCase(self.store_repository)
        self.uc_list_categories = ListCategoriesUseCase(self.category_repository)
        self.uc_get_by_id_category = UCGetByIdCategory(self.category_repository)

    async def create_category(self, category: CategoryInputDto) -> CategoryOutputDto:
        store = await self.uc_get_store.execute(category.store_slug)
        category_on_db = await self.uc_create_category.execute(
            Category(name=category.name, store_id=str(store.id)),
        )
        return CategoryOutputDto(
            id=category_on_db.id,
            name=category_on_db.name,
            store_id=str(store.id),
        )

    async def get_category_by_id(self, id: str) -> CategoryOutputDto:
        category_on_db = await self.uc_get_by_id_category.execute(id)
        return CategoryOutputDto(
            id=category_on_db.id,
            name=category_on_db.name,
            store_id=str(category_on_db.store_id),
        )

    async def list_categories(self, store_slug: str) -> CategoryListOutputDto:
        store = await self.uc_get_store.execute(store_slug)
        categories = await self.uc_list_categories.execute(store.id)
        return CategoryListOutputDto(
            data=[
                CategoryOutputDto(
                    id=category.id,
                    name=category.name,
                    store_id=str(category.store_id),
                )
                for category in categories
            ],
        )
