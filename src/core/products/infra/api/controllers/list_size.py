from ninja import NinjaAPI

from src.core.products.application.services.service_size import SizeService
from src.core.products.infra.database.django.repository import DjangoSizeRepository
from src.core.store.infra.database.django.repository import DjangoStoreRepository


async def list_sizes(request: NinjaAPI, store_slug: str):
    service = SizeService(DjangoSizeRepository(), DjangoStoreRepository())
    return await service.list_sizes(store_slug)
