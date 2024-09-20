from abc import ABC, abstractmethod

from src.core.user.domain.dto.user_dto import UserInput, UserOutput


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: UserInput) -> UserOutput:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserOutput:
        pass
