from src.core.store.application.services.store_service import StoreService
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.user.infra.database.repository import DjangoUserRepository
from core.storage.infra.tebi_io.tebi_io_repository import TebiIOStorageRepository


async def delete(
    request,
    id: str,
):
    try:

        service = StoreService(
            store_repository=DjangoStoreRepository(),
            storage_repository=TebiIOStorageRepository(),
            user_repository=DjangoUserRepository(),
        )

        await service.delete_store(id)
        return 204, None

    except Exception as e:
        if hasattr(e, "status_code"):
            return e.status_code, {"message": str(e.msg)}
        return 500, {"message": str(e)}
