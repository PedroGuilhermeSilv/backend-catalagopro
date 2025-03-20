from core.user.infra.interfaces.repository import UserRepository
from src.core.user.domain.dto import UserOutput


class GetUserById:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> UserOutput:
        return await self.repository.get_by_id(id)
