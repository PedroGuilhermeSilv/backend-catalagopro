from ninja import NinjaAPI

from src.core.products.application.services.dto import CategoryInputDto
from src.core.products.application.services.service_category import CategoryService
from src.core.products.infra.database.django.repository import (
    DjangoCategoryRepository,
)
from src.core.store.infra.database.django.repository import DjangoStoreRepository


async def create_category(request: NinjaAPI, category: CategoryInputDto):
    try:
        category_service = CategoryService(
            category_repository=DjangoCategoryRepository(),
            store_repository=DjangoStoreRepository(),
        )
        category_output = await category_service.create_category(category)
        return 201, category_output
    except Exception as e:
        return 400, {"message": str(e)}
