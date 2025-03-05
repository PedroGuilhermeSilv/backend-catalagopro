from typing import Union
from src.core.user.domain.repository import UserRepository, UserOutput


class UseCaseListUsers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> Union[list[UserOutput], None]:
        return await self.repository.list()
