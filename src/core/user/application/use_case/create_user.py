from src.core.user.application.service.dto import (
    InputServiceCreateUser,
    OutputCreateUser,
    OutputServiceCreateUser,
)
from src.core.user.domain.dto import UserInput
from src.core.user.domain.entity import User
from src.core.user.domain.exceptions import UserAlreadyExistError
from src.core.user.infra.interfaces.repository import UserRepository


class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, input: InputServiceCreateUser) -> OutputServiceCreateUser:
        if user := await self.repository.get_by_email(input.email):
            raise UserAlreadyExistError

        try:
            user = User(
                email=input.email,
                password=input.password,
                role=input.role.value,
                name=input.name,
                store_slug=input.store_slug,
                status=input.status.value,
            )
            user = await self.repository.save(
                UserInput(
                    **{
                        **user.model_dump(),
                        "role": user.role.value,
                        "status": user.status.value,
                    },
                ),
            )
        except Exception as error:
            raise error

        # Criar o objeto de saída
        return OutputCreateUser(
            email=user.email,
            id=user.id,
            role=user.role.value,
            store_slug=user.store_slug,
            name=user.name,
            status=user.status.value,
        )
