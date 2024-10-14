from src.core.user.application.service.dto.user_dto import (
    InputServiceCreateUser,
    OutputCreateUser,
    OutputServiceCreateUser,
)
from src.core.user.domain.dto import UserInput
from src.core.user.domain.entity import User
from src.core.user.domain.exceptions import UserAlreadyExistError
from src.core.user.domain.repository import UserRepository


class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: InputServiceCreateUser) -> OutputServiceCreateUser:
        if user := await self.repository.get_by_email(input.email):
            raise UserAlreadyExistError

        try:
            user = User(email=input.email, password=input.password)
            user = await self.repository.save(UserInput(**user.model_dump()))
        except Exception as error:
            raise error
        return OutputCreateUser(email=user.email, id=user.id)
