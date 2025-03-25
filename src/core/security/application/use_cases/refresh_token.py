from src.core.security.application.service.dto.jwt import (
    InputRefreshToken,
    JwtOutPutDto,
)
from src.core.shared.exceptions.erros import UserNotFoundError
from src.core.shared.token import create_token, verify_token
from src.core.user.infra.interfaces.repository import UserRepository


class JWTRefresh:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: InputRefreshToken) -> JwtOutPutDto:
        try:
            payload = verify_token(input.refresh_token)
            user = await self.repository.get_by_email(payload["email"])
            if not user:
                raise UserNotFoundError

            token = create_token({"email": payload["email"]}, expires_in=60)

        except Exception as error:
            raise error
        return JwtOutPutDto(token=token, refresh_token=input.refresh_token, exp=60)
