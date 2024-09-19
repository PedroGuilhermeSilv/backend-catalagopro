from ninja import Router
from src.core.user.application.service.create_user import (
    CreateUser,
    InputServiceCreateUser,
)
from src.core.user.infra.django.user.application.controllers.dto.erros import (
    Error,
    UserCreateDto,
    UserOutputDto,
)
from src.core.user.infra.django.user.repositories.user_repository import (
    DjangoUserRepository,
)

router = Router()


@router.post("/", response={201: UserOutputDto, 409: Error})
async def create(request, user: UserCreateDto):
    try:
        service = CreateUser(repository=DjangoUserRepository())
        response = await service.execute(input=InputServiceCreateUser(**user.dict()))
    except Exception as e:
        return 409, {"error": str(e)}

    return response
