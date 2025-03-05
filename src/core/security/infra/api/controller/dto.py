from ninja import Router

from src.core.security.application.use_cases.create_token import JWTCreator
from src.core.security.application.service.dto.jwt import (
    InputAuthUserDto,
    InputRefreshToken,
)
from src.core.security.application.service.security_service import SecurityService
from core.security.infra.api.controller.schemas import (
    InputRefreshTokenDto,
    LoginInputDto,
    LoginOutputDto,
    response,
)
from core.user.infra.database.repository import DjangoUserRepository

router = Router(tags=["Auth"])


@router.post("/login/", response=response)
async def login(request, login: LoginInputDto) -> LoginOutputDto:
    try:
        service = SecurityService(repository=DjangoUserRepository())
        response = await service.create_token(input=InputAuthUserDto(**login.dict()))
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, response


@router.post("/refresh/", response=response)
async def refresh(request, token: InputRefreshTokenDto) -> LoginOutputDto:
    try:
        service = SecurityService(repository=DjangoUserRepository())
        response = await service.create_refresh_token(
            input=InputRefreshToken(refresh_token=token.token),
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, response
