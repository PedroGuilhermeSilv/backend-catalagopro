from src.core.store.domain.entity import Store, BusinessHour
from src.core.store.domain.repository import StoreRepository
from src.core.store.infra.database.models import (
    Store as StoreModel,
)
from datetime import datetime
from src.core.user.infra.database.models import User as UserModel

class DjangoStoreRepository(StoreRepository):
    def __init__(self):
        self.model_store = StoreModel
        self.model_user = UserModel
    def _convert_to_domain(self, store_model: StoreModel) -> Store:
        """Converte o modelo Django para a entidade do domínio"""
        store_data = {
            "id": store_model.id,
            "name": store_model.name,
            "owner_id": str(store_model.owner_id),
            "created_at": datetime.combine(store_model.created_at, datetime.min.time()),
            "updated_at": datetime.combine(store_model.updated_at, datetime.min.time()),
            "slug": store_model.slug,
            "logo_url": store_model.logo_url,
            "description": store_model.description,
            "address": store_model.address,
            "whatsapp": store_model.whatsapp,
            "business_hours": [
                BusinessHour(
                    day=hour["day"],
                    open_hour=hour["open_hour"],
                    close_hour=hour["close_hour"],
                )
                for hour in store_model.business_hours
            ],
        }
        return Store(**store_data)

    async def save(self, store: Store) -> Store:
        store_data = store.model_dump()
        user = await self.model_user.objects.aget(id=store_data["owner_id"])
        store_data["owner_id"] = user

        store_model = await self.model_store.objects.acreate(**store_data)

        return self._convert_to_domain(store_model)

    async def get_by_id(self, id: str) -> Store:
        store_model = await self.model_store.objects.aget(id=id)
        return self._convert_to_domain(store_model)

    async def get_by_slug(self, slug: str) -> Store:
        store_model = await self.model_store.objects.aget(slug=slug)
        return self._convert_to_domain(store_model)
