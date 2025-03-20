from datetime import datetime

from asgiref.sync import sync_to_async
from src.core.store.domain.dtos import StoreListDto
from src.core.store.domain.entity import BusinessHour, Store
from src.core.store.infra.database.models import (
    Store as StoreModel,
)
from src.core.user.infra.database.models import User as UserModel

from core.store.infra.interfaces.repository import StoreRepository


class DjangoStoreRepository(StoreRepository):
    def __init__(self):
        self.model_store = StoreModel
        self.model_user = UserModel

    async def _convert_to_domain(self, store_model: StoreModel) -> Store:
        """Converte o modelo Django para a entidade do domínio"""
        # Using async access for related field
        owner = await self.model_user.objects.aget(id=store_model.owner_id_id)

        store_data = {
            "id": str(store_model.id),
            "name": store_model.name,
            "owner_id": str(owner.id),
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
            "status": store_model.status,
        }
        return Store(**store_data)

    async def save(self, store: Store) -> Store:
        store_data = store.model_dump()
        user = await self.model_user.objects.aget(id=store_data["owner_id"])
        store_data["owner_id"] = user

        store_model = await self.model_store.objects.acreate(**store_data)

        return await self._convert_to_domain(store_model)

    async def get_by_id(self, id: str) -> Store:
        store_model = await self.model_store.objects.aget(id=id)
        return await self._convert_to_domain(store_model)

    async def get_by_slug(self, slug: str) -> Store:
        store_model = await self.model_store.objects.aget(slug=slug)
        return await self._convert_to_domain(store_model)

    async def list(self) -> list[StoreListDto]:
        store_models = await sync_to_async(list)(self.model_store.objects.all())
        result = []
        for model in store_models:
            result.append(await self._convert_to_domain(model))
        return result
