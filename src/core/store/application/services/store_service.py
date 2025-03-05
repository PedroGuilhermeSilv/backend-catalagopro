from src.core.utils.date import BusinessHour
from src.core.storage.application.use_case.save_file import SaveFile
from src.core.storage.domain.repository import StorageRepository
from src.core.store.domain.repository import StoreRepository
from src.core.store.application.use_case.create_store import CreateStoreUseCase
from src.core.store.domain.entity import Store
from src.core.store.application.services.dtos import InputServiceCreateStore
from src.core.storage.application.use_case.dto import SaveFileInput
from src.core.user.application.use_case.get_user_by_email import GetUserByEmail
from src.core.user.domain.repository import UserRepository


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

    async def create_store(self, input: InputServiceCreateStore) -> Store:
        try:
            file_output = self.save_file.execute(SaveFileInput(file=input.image))
            file_url = file_output.file_url

            user = await self.get_user_by_email.execute(input.email_owner)

            return await self.save_store.execute(
                Store(
                    name=input.name,
                    owner_id=str(user.id),
                    logo_url=file_url,
                    description=input.description,
                    address=input.address,
                    whatsapp=input.whatsapp,
                    business_hours=[
                        BusinessHour(
                            day=hour.day.value,
                            open_hour=hour.open_hour,
                            close_hour=hour.close_hour,
                        )
                        for hour in input.business_hours
                    ],
                )
            )
        except Exception as e:
            raise e
