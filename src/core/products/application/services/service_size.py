from src.core.products.application.services.dto import (
    SizeInputDto,
    SizeListOutputDto,
    SizeOutputDto,
)
from src.core.products.application.use_case.uc_create_size import CreateSizeUseCase
from src.core.products.application.use_case.uc_list_sizes import ListSizesUseCase
from src.core.products.domain.entity import Size
from src.core.products.infra.database.repository import SizeRepository
from src.core.store.application.use_case.get_by_slug import GetStoreBySlugUseCase
from src.core.store.infra.database.repository import StoreRepository


class SizeService:
    def __init__(
        self, size_repository: SizeRepository, store_repository: StoreRepository,
    ):
        self.size_repository = size_repository
        self.store_repository = store_repository
        self.uc_get_store = GetStoreBySlugUseCase(store_repository)
        self.uc_create_size = CreateSizeUseCase(size_repository)
        self.uc_list_sizes = ListSizesUseCase(size_repository)

    async def create_size(self, size: SizeInputDto) -> SizeOutputDto:
        store = await self.uc_get_store.execute(size.store_slug)
        result = await self.uc_create_size.execute(
            Size(name=size.name, store_id=str(store.id)),
        )
        return SizeOutputDto(id=result.id, name=result.name, store_id=str(store.id))

    async def list_sizes(self, store_slug: str) -> SizeListOutputDto:
        store = await self.uc_get_store.execute(store_slug)
        sizes = await self.uc_list_sizes.execute(str(store.id))
        return SizeListOutputDto(
            data=[
                SizeOutputDto(id=size.id, name=size.name, store_id=str(size.store_id))
                for size in sizes
            ],
        )
