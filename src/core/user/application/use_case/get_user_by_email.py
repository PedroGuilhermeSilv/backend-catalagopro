from src.core.user.domain.dto import UserOutput
from src.core.user.domain.repository import UserRepository


class GetUserByEmail:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, email: str) -> UserOutput:
        return await self.repository.get_by_email(email)
