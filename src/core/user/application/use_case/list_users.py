from core.user.infra.interfaces.repository import UserOutput, UserRepository


class UseCaseListUsers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> list[UserOutput] | None:
        return await self.repository.list()
