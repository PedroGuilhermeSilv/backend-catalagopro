from src.core.storage.application.use_case.dto import SaveFileInput
from src.core.storage.application.use_case.save_file import SaveFile
from src.core.storage.infra.interfaces.repository import StorageRepository
from src.core.store.application.services.dtos import (
    InputServiceCreateStore,
    InputServiceUpdateStore,
    OutputServiceListStore,
)
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.application.use_case.delete_store import DeleteStoreUseCase
from src.core.store.application.use_case.get_store_by_id import GetStoreByIdUseCase
from src.core.store.application.use_case.list_store import ListStoreUseCase
from src.core.store.application.use_case.update_store import UpdateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.domain.enums import BusinessHour
from src.core.store.infra.interfaces.repository import StoreRepository
from src.core.user.application.use_case.get_user_by_email import GetUserByEmail
from src.core.user.application.use_case.get_user_by_id import GetUserById
from src.core.user.infra.interfaces.repository import UserRepository


class StoreService:
    def __init__(
        self,
        store_repository: StoreRepository,
        storage_repository: StorageRepository,
        user_repository: UserRepository,
    ):
        self.uc_save_store = CreateStoreUseCase(store_repository)
        self.uc_save_file = SaveFile(storage_repository)
        self.uc_get_user_by_email = GetUserByEmail(user_repository)
        self.uc_get_all_stores = ListStoreUseCase(store_repository)
        self.uc_get_user_by_id = GetUserById(user_repository)
        self.uc_get_store_by_id = GetStoreByIdUseCase(store_repository)
        self.uc_update_store = UpdateStoreUseCase(store_repository)
        self.uc_delete_store = DeleteStoreUseCase(store_repository)

    async def create_store(self, input: InputServiceCreateStore) -> Store:
        try:
            user = await self.uc_get_user_by_email.execute(input.email_owner)
            store = Store(
                name=input.name,
                owner_id=str(user.id),
                logo_url="",
                description=input.description,
                address=input.address,
                whatsapp=input.whatsapp,
                status=input.status,
                business_hours=[
                    BusinessHour(
                        day=hour.day.value,
                        open_hour=hour.open_hour,
                        close_hour=hour.close_hour,
                    )
                    for hour in input.business_hours
                ],
            )

            file_output = self.uc_save_file.execute(
                SaveFileInput(file=input.image),
                str(store.id),
            )
            store.logo_url = file_output.file_url

            return await self.uc_save_store.execute(store)
        except Exception as e:
            raise e

    async def list_stores(self) -> OutputServiceListStore:
        stores = await self.uc_get_all_stores.execute()
        return OutputServiceListStore(
            data=[
                {
                    "id": store.id,
                    "name": store.name,
                    "slug": store.slug,
                    "created_at": store.created_at,
                    "updated_at": store.updated_at,
                    "status": store.status.value,
                    "logo_url": store.logo_url,
                    "description": store.description,
                    "address": store.address,
                    "whatsapp": store.whatsapp,
                    "business_hours": [
                        {
                            "day": hour.day.value,
                            "open_hour": hour.formatted_open_hour,
                            "close_hour": hour.formatted_close_hour,
                        }
                        for hour in store.business_hours
                    ],
                    "owner_id": store.owner_id,
                    "owner_name": (
                        await self.uc_get_user_by_id.execute(store.owner_id)
                    ).name,
                }
                for store in stores
            ],
        )

    async def update_store(self, input: InputServiceUpdateStore) -> Store:
        try:
            store_on_db = await self.uc_get_store_by_id.execute(input.store_id)
            if input.image:
                store_on_db.logo_url = self.storage_repository.update_file(
                    SaveFileInput(file=input.image),
                    str(store_on_db.id),
                )
            if input.owner_id:
                owner = await self.uc_get_user_by_id.execute(input.owner_id)
                store_on_db.owner_id = str(owner.id)

            store = Store(
                id=input.store_id if input.store_id else store_on_db.id,
                name=input.name if input.name else store_on_db.name,
                slug=input.slug if input.slug else store_on_db.slug,
                logo_url=store_on_db.logo_url,
                description=(
                    input.description if input.description else store_on_db.description
                ),
                address=input.address if input.address else store_on_db.address,
                whatsapp=input.whatsapp if input.whatsapp else store_on_db.whatsapp,
                business_hours=(
                    [
                        BusinessHour(
                            day=hour.day.value,
                            open_hour=hour.open_hour,
                            close_hour=hour.close_hour,
                        )
                        for hour in input.business_hours
                    ]
                    if input.business_hours
                    else store_on_db.business_hours
                ),
                status=input.status if input.status else store_on_db.status,
                owner_id=store_on_db.owner_id,
            )
            return await self.uc_update_store.execute(store)
        except Exception as e:
            raise e

    async def delete_store(self, store_id: str) -> None:
        try:
            await self.uc_delete_store.execute(store_id)
        except Exception as e:
            raise e
