from abc import ABC, abstractmethod

from src.core.user.domain.dto import UserInput, UserOutput


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserInput) -> UserOutput:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserOutput | None:
        pass

    @abstractmethod
    async def list(self) -> list[UserOutput]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass

    @abstractmethod
    async def update(self, user: UserInput) -> UserOutput:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> UserOutput | None:
        pass
