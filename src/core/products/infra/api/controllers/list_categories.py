from ninja import NinjaAPI

from src.core.products.application.services.service_category import CategoryService
from src.core.products.infra.database.django.repository import (
    DjangoCategoryRepository,
)
from src.core.store.infra.database.django.repository import DjangoStoreRepository


async def list_categories(request: NinjaAPI, store_slug: str):
    service = CategoryService(DjangoCategoryRepository(), DjangoStoreRepository())
    return await service.list_categories(store_slug)
