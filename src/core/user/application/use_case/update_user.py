from src.core.user.domain.dto import UserInput, UserOutput
from src.core.user.infra.interfaces.repository import UserRepository


class UpdateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: UserInput) -> UserOutput:
        try:
            return await self.repository.update(input)
        except Exception as e:
            raise e
