from src.core.user.domain.exceptions.user_exceptions import (
    UserNotFoundError,
)
from src.core.user.domain.repository.user_repository import UserRepository
from src.core.utils.security.application.dto.jwt import InputAuthUserDto, JwtDto
from src.core.utils.security.hash import verify_password
from src.core.utils.security.jwt import create_jwt


class JWTCreator:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: InputAuthUserDto) -> JwtDto:
        user = await self.repository.get_by_email(input.email)
        if not user:
            raise UserNotFoundError

        try:
            if not verify_password(input.password, user.password):
                raise UserNotFoundError
            payload = {"email": user.email}
            token = create_jwt(payload, expires_in=60)

        except Exception as error:
            raise error
        return JwtDto(token=token, exp=60)
