from src.core.store.domain.dtos import StoreListDto
from src.core.store.domain.entity import Store

from core.store.infra.interfaces.repository import StoreRepository


class InMemoryStoreRepository(StoreRepository):
    def __init__(self, stores: list[Store] = []):
        self.stores = stores

    async def save(self, store: Store) -> Store:
        self.stores.append(store)
        return store

    async def get_by_id(self, id: str) -> Store:
        return next((store for store in self.stores if store.id == id), None)

    async def get_by_slug(self, slug: str) -> Store:
        return next((store for store in self.stores if store.slug == slug), None)

    async def list(self) -> list[StoreListDto]:
        return [
            StoreListDto(
                id=store.id,
                name=store.name,
                slug=store.slug,
                created_at=store.created_at,
                updated_at=store.updated_at,
                status=store.status,
                logo_url=store.logo_url,
                description=store.description,
                address=store.address,
                whatsapp=store.whatsapp,
                business_hours=store.business_hours,
                owner_id=store.owner_id,
            )
            for store in self.stores
        ]
