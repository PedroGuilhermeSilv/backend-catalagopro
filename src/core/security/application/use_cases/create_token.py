from src.core.security.application.service.dto.jwt import InputAuthUserDto, JwtOutPutDto
from src.core.user.infra.interfaces.repository import UserRepository
from src.core.utils.exceptions.erros import InvalidPasswordError, UserNotFoundError
from src.core.utils.hash import verify_password
from src.core.utils.token import create_refresh_token, create_token


class JWTCreator:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: InputAuthUserDto) -> JwtOutPutDto:
        user = await self.repository.get_by_email(input.email)
        if not user:
            raise UserNotFoundError

        try:
            if not verify_password(input.password, user.password):
                raise InvalidPasswordError
            payload = {
                "email": user.email,
                "tenant": user.store_slug if user.store_slug else None,
                "role": user.role.value if user.role else None,
            }
            token = create_token(payload, expires_in=60)
            refresh_token = create_refresh_token(payload)

        except Exception as error:
            raise error
        return JwtOutPutDto(token=token, refresh_token=refresh_token, exp=60)
