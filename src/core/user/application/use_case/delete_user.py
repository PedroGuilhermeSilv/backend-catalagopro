from core.user.infra.interfaces.repository import UserRepository


class DeleteUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, id: str) -> None:
        return await self.repository.delete(id)
