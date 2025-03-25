from src.core.store.domain.dtos import StoreListDto
from src.core.store.domain.entity import Store
from src.core.store.domain.exceptions import StoreNotFoundError
from src.core.store.infra.interfaces.repository import StoreRepository


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

    async def update(self, store: Store) -> Store:
        for index, value in enumerate(self.stores):
            if value.id == store.id:
                self.stores[index] = store
                return store
        raise StoreNotFoundError

    async def delete(self, id: str) -> None:
        self.stores = [store for store in self.stores if store.id != id]
