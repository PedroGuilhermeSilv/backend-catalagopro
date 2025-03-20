from src.core.storage.application.use_case.dto import SaveFileInput
from src.core.storage.application.use_case.save_file import SaveFile
from src.core.store.application.services.dtos import (
    BusinessHourCreateDto,
    InputServiceCreateStore,
    OutputServiceListStore,
)
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.application.use_case.list_store import ListStoreUseCase
from src.core.store.domain.entity import Store
from src.core.user.application.use_case.get_user_by_email import GetUserByEmail
from src.core.utils.date import BusinessHour

from core.storage.infra.interfaces.repository import StorageRepository
from core.store.infra.interfaces.repository import StoreRepository
from core.user.application.use_case.get_user_by_id import GetUserById
from core.user.infra.interfaces.repository import UserRepository


class StoreService:
    def __init__(
        self,
        store_repository: StoreRepository,
        storage_repository: StorageRepository,
        user_repository: UserRepository,
    ):
        self.save_store = CreateStoreUseCase(store_repository)
        self.save_file = SaveFile(storage_repository)
        self.get_user_by_email = GetUserByEmail(user_repository)
        self.get_all_stores = ListStoreUseCase(store_repository)
        self.get_user_by_id = GetUserById(user_repository)

    async def create_store(self, input: InputServiceCreateStore) -> Store:
        try:
            user = await self.get_user_by_email.execute(input.email_owner)

            file_output = self.save_file.execute(
                SaveFileInput(file=input.image),
                str(user.id),
            )
            file_url = file_output.file_url

            return await self.save_store.execute(
                Store(
                    name=input.name,
                    owner_id=str(user.id),
                    logo_url=file_url,
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
                ),
            )
        except Exception as e:
            raise e

    async def list_stores(self) -> OutputServiceListStore:
        stores = await self.get_all_stores.execute()
        return OutputServiceListStore(
            data=[
                {
                    "id": store.id,
                    "name": store.name,
                    "slug": store.slug,
                    "created_at": store.created_at,
                    "updated_at": store.updated_at,
                    "status": store.status,
                    "logo_url": store.logo_url,
                    "description": store.description,
                    "address": store.address,
                    "whatsapp": store.whatsapp,
                    "business_hours": [
                        BusinessHourCreateDto(
                            day=hour.day.value,
                            open_hour=hour.formatted_open_hour,
                            close_hour=hour.formatted_close_hour,
                        )
                        for hour in store.business_hours
                    ],
                    "owner_id": store.owner_id,
                    "owner_name": (
                        await self.get_user_by_id.execute(store.owner_id)
                    ).name,
                }
                for store in stores
            ],
        )
