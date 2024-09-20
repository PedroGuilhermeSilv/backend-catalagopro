from ninja import Router
from src.core.security.application.service.auth_jwt import JWTCreator
from src.core.security.application.service.dto.jwt import InputAuthUserDto
from src.core.security.infra.django.security.application.controller.dto.schemas import (
    LoginInputDto,
    response,
)
from src.core.user.infra.django.user.repositories.user_repository import (
    DjangoUserRepository,
)

router = Router()


@router.post("/login/", response=response)
async def login(request, login: LoginInputDto):
    try:
        service = JWTCreator(repository=DjangoUserRepository())
        response = await service.execute(input=InputAuthUserDto(**login.dict()))
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, response
