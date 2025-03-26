from src.core.products.domain.entity import Category, Size
from src.core.products.infra.database.django.models import (
    Category as CategoryModel,
)
from src.core.products.infra.database.django.models import (
    Size as SizeModel,
)
from src.core.products.infra.database.repository import (
    CategoryRepository,
    SizeRepository,
)


class DjangoCategoryRepository(CategoryRepository):
    def __init__(self):
        self.model = CategoryModel

    def create(self, category: Category) -> Category:
        category_model = self.model.objects.create(name=category.name)
        return Category(
            id=str(category_model.id),
            name=category_model.name,
        )


class DjangoSizeRepository(SizeRepository):
    def __init__(self):
        self.model = SizeModel

    def create(self, size: Size) -> Size:
        size_model = self.model.objects.create(name=size.name)
        return Size(
            id=str(size_model.id),
            name=size_model.name,
        )
