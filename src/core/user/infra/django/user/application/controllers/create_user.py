from ninja import Router

from src.core.user.application.service.create_user import (
    CreateUser,
    InputServiceCreateUser,
)
from src.core.user.infra.django.user.application.controllers.dto.schemas import (
    UserCreateDto,
    response,
)
from src.core.user.infra.django.user.repositories.user_repository import (
    DjangoUserRepository,
)

router = Router()


@router.post("/", response=response)
async def create(request, user: UserCreateDto):
    try:
        service = CreateUser(repository=DjangoUserRepository())
        response = await service.execute(input=InputServiceCreateUser(**user.dict()))
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 201, response
