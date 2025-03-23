from datetime import datetime

from asgiref.sync import sync_to_async
from src.core.store.domain.dtos import StoreListDto
from src.core.store.domain.entity import BusinessHour, Store
from src.core.store.infra.database.models import (
    Store as StoreModel,
)
from src.core.user.infra.database.models import User as UserModel

from core.store.domain.exceptions import StoreNotFoundError
from core.store.infra.interfaces.repository import StoreRepository
from core.user.domain.exceptions import UserNotFoundError


class DjangoStoreRepository(StoreRepository):
    def __init__(self):
        self.model_store = StoreModel
        self.model_user = UserModel

    async def _convert_to_domain(self, store_model: StoreModel) -> Store:
        """Converte o modelo Django para a entidade do domínio"""
        # Using async access for related field

        if isinstance(store_model.owner_id, str):
            user = await self.model_user.objects.aget(id=store_model.owner_id)
            store_model.owner_id = user
        store_data = {
            "id": str(store_model.id),
            "name": store_model.name,
            "owner_id": str(store_model.owner_id.id),
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
        try:
            store_model = await self.model_store.objects.aget(id=id)
            user = await self.model_user.objects.aget(id=store_model.owner_id_id)
            store_model.owner_id = user
        except Exception as e:
            raise StoreNotFoundError from e
        return await self._convert_to_domain(store_model)

    async def get_by_slug(self, slug: str) -> Store:
        store_model = await self.model_store.objects.aget(slug=slug)
        user = await self.model_user.objects.aget(id=store_model.owner_id_id)
        store_model.owner_id = user
        return await self._convert_to_domain(store_model)

    async def list(self) -> list[StoreListDto]:
        store_models = await sync_to_async(list)(self.model_store.objects.all())

        result = []
        for model in store_models:
            try:
                user = await self.model_user.objects.aget(id=model.owner_id_id)
                model.owner_id = user
            except Exception as e:
                raise UserNotFoundError from e

            result.append(await self._convert_to_domain(model))

        return result

    async def update(self, store: Store) -> Store:
        try:
            user = await self.model_user.objects.aget(id=store.owner_id)
        except UserNotFoundError as e:
            raise UserNotFoundError from e

        try:
            await self.model_store.objects.filter(id=store.id).aupdate(
                name=store.name,
                slug=store.slug,
                logo_url=store.logo_url,
                description=store.description,
                address=store.address,
                whatsapp=store.whatsapp,
                business_hours=[hour.model_dump() for hour in store.business_hours],
                status=store.status,
                owner_id=user,
                created_at=store.created_at,
                updated_at=store.updated_at,
            )

            store_model = await self.model_store.objects.aget(id=store.id)
            store_model.owner_id = user
        except Exception as e:
            raise StoreNotFoundError from e
        return await self._convert_to_domain(store_model)

    async def delete(self, id: str) -> None:
        try:
            store = await self.model_store.objects.aget(id=id)
            await store.adelete()
        except Exception as e:
            raise StoreNotFoundError from e
