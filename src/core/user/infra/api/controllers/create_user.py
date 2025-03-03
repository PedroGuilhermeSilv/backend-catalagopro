from ninja import Router

from core.user.application.use_case.create_user import (
    CreateUser,
    InputServiceCreateUser,
)
from src.core.user.application.service.user_service import UserService
from src.core.user.infra.api.controllers.dto.schemas import (
    UserCreateDto,
    response,
)
from core.user.infra.api.repository import (
    DjangoUserRepository,
)

router = Router()


@router.post("/", response=response)
async def create(request, user: UserCreateDto):
    try:
        service = UserService(repository=DjangoUserRepository())
        response = await service.create_user(
            input=InputServiceCreateUser(**user.dict())
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 201, response
