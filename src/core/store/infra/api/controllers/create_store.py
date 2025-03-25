import json

from ninja import File, Form
from ninja.files import UploadedFile
from src.core.shared.enums import Status
from src.core.shared.file import UploadedFile as DomainUploadedFile
from src.core.storage.infra.tebi_io.tebi_io_repository import TebiIOStorageRepository
from src.core.store.application.services.dtos import InputServiceCreateStore
from src.core.store.application.services.store_service import StoreService
from src.core.store.infra.api.controllers.dtos import (
    StoreCreateOutputDto,
)
from src.core.store.infra.database.repository import DjangoStoreRepository
from src.core.user.infra.database.repository import DjangoUserRepository


async def create(
    request,
    image: UploadedFile = File(...),
    name: str = Form(...),
    email_owner: str = Form(...),
    description: str = Form(...),
    address: str = Form(...),
    whatsapp: str = Form(...),
    business_hours: str = Form(...),
    status: Status = Form(...),
):
    try:
        business_hours_list = json.loads(business_hours)
        input_service = {
            "name": name,
            "description": description,
            "address": address,
            "whatsapp": whatsapp,
            "business_hours": business_hours_list,
            "image": DomainUploadedFile.from_upload(image),
            "email_owner": email_owner,
            "status": status,
        }
        service = StoreService(
            store_repository=DjangoStoreRepository(),
            storage_repository=TebiIOStorageRepository(),
            user_repository=DjangoUserRepository(),
        )
        response = await service.create_store(
            input=InputServiceCreateStore(**input_service),
        )
    except Exception as e:
        if hasattr(e, "status_code"):
            return e.status_code, {"message": str(e.msg)}
        return 500, {"message": str(e)}
    return 201, StoreCreateOutputDto(**response.model_dump())
