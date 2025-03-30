from asgiref.sync import sync_to_async

from src.core.products.domain.entity import Category, Size
from src.core.products.infra.database.django.models import (
    Category as CategoryModel,
)
from src.core.products.infra.database.django.models import (
    Size as SizeModel,
)
from src.core.products.infra.database.django.models import (
    Store as StoreModel,
)
from src.core.products.infra.database.repository import (
    CategoryRepository,
    SizeRepository,
)


class DjangoCategoryRepository(CategoryRepository):
    def __init__(self):
        self.model = CategoryModel

    async def create(self, category: Category) -> Category:
        store = await StoreModel.objects.aget(id=category.store_id)
        category_model = await self.model.objects.acreate(
            name=category.name,
            store=store,
        )
        return Category(
            id=str(category_model.id),
            name=category_model.name,
            store_id=str(category_model.store_id),
        )

    async def list(self, store_id: str) -> list[Category]:
        get_categories = sync_to_async(
            lambda: list(self.model.objects.filter(store_id=store_id)),
        )
        categories = await get_categories()
        return [
            Category(
                id=str(category.id),
                name=category.name,
                store_id=str(category.store_id),
            )
            for category in categories
        ]


class DjangoSizeRepository(SizeRepository):
    def __init__(self):
        self.model = SizeModel

    async def create(self, size: Size) -> Size:
        store = await StoreModel.objects.aget(id=size.store_id)
        size_model = await self.model.objects.acreate(
            name=size.name,
            store=store,
        )
        return Size(
            id=str(size_model.id),
            name=size_model.name,
            store_id=str(size_model.store_id),
        )

    async def list(self, store_id: str) -> list[Size]:
        get_sizes = sync_to_async(
            lambda: list(self.model.objects.filter(store_id=store_id)),
        )
        sizes = await get_sizes()
        return [
            Size(id=str(size.id), name=size.name, store_id=str(size.store_id))
            for size in sizes
        ]
