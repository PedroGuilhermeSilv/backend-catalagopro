from ninja import Router

from src.core.security.application.service.create_token import JWTCreator
from src.core.security.application.service.dto.jwt import InputAuthUserDto
from src.core.security.application.service.refresh_token import (
    InputRefreshToken,
    JWTRefresh,
)
from src.core.security.infra.django.security.application.controller.dto.schemas import (
    InputRefreshTokenDto,
    LoginInputDto,
    LoginOutputDto,
    response,
)
from src.core.user.infra.django.repositories.user_repository import DjangoUserRepository

router = Router()


@router.post("/login/", response=response)
async def login(request, login: LoginInputDto) -> LoginOutputDto:
    try:
        service = JWTCreator(repository=DjangoUserRepository())
        response = await service.execute(input=InputAuthUserDto(**login.dict()))
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, response


@router.post("/refresh/", response=response)
async def refresh(request, token: InputRefreshTokenDto) -> LoginOutputDto:
    try:
        service = JWTRefresh(repository=DjangoUserRepository())
        response = await service.execute(
            input=InputRefreshToken(refresh_token=token.token),
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, response
