from src.core.storage.infra.tebi_io.domain.repository import TebiIOStorageRepository
from src.core.store.application.services.store_service import StoreService
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.user.infra.database.repository import DjangoUserRepository


async def list(
    request,
):
    try:
        service = StoreService(
            store_repository=DjangoStoreRepository(),
            storage_repository=TebiIOStorageRepository(),
            user_repository=DjangoUserRepository(),
        )
        response = await service.list_stores()
        return 200, response
    except Exception as e:
        return 500, {"message": str(e)}
