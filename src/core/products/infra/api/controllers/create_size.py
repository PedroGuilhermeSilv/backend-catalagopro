from ninja import NinjaAPI

from src.core.products.application.services.service_size import SizeService
from src.core.products.infra.api.controllers.dto import SizeInputDto
from src.core.products.infra.database.django.repository import DjangoSizeRepository
from src.core.store.infra.database.django.repository import DjangoStoreRepository


async def create_size(request: NinjaAPI, size: SizeInputDto):
    try:
        size_service = SizeService(
            size_repository=DjangoSizeRepository(),
            store_repository=DjangoStoreRepository(),
        )
        size_output = await size_service.create_size(size)
        return 201, size_output
    except Exception as e:
        return 400, {"message": str(e)}
