from src.core.security.application.service.dto.jwt import (
    InputAuthUserDto,
    InputRefreshToken,
    JwtOutPutDto,
)
from src.core.security.application.use_cases.refresh_token import (
    JWTRefresh,
)
from src.core.security.application.use_cases.create_token import (
    JWTCreator,
)
from src.core.user.domain.repository import UserRepository


class SecurityService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.create_token_use_case = JWTCreator(self.repository)
        self.create_refresh_token_use_case = JWTRefresh(self.repository)

    async def create_token(self, input: InputAuthUserDto) -> JwtOutPutDto:
        return await self.create_token_use_case.execute(input)

    async def create_refresh_token(self, input: InputRefreshToken) -> JwtOutPutDto:
        return await self.create_refresh_token_use_case.execute(input)
