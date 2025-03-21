from core.user.application.use_case.get_user_by_id import GetUserById
from core.user.application.use_case.update_user import UpdateUser
from core.user.infra.interfaces.repository import UserRepository
from src.core.user.application.service.dto import (
    InputDeleteUser,
    InputServiceCreateUser,
    InputUpdateUser,
)
from src.core.user.application.use_case.create_user import CreateUser
from src.core.user.application.use_case.delete_user import DeleteUser
from src.core.user.application.use_case.get_user_by_email import GetUserByEmail
from src.core.user.application.use_case.list_users import UseCaseListUsers
from src.core.user.application.use_case.update_user import UserInput
from src.core.user.domain.exceptions import UserNotFoundError


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.create_user_use_case = CreateUser(self.repository)
        self.list_users_use_case = UseCaseListUsers(self.repository)
        self.delete_user_use_case = DeleteUser(self.repository)
        self.update_user_use_case = UpdateUser(self.repository)
        self.get_user_by_id_use_case = GetUserById(self.repository)
        self.get_user_by_email_use_case = GetUserByEmail(self.repository)

    async def create_user(self, input: InputServiceCreateUser):
        return await self.create_user_use_case.execute(input)

    async def list_users(self):
        return await self.list_users_use_case.execute()

    async def delete_user(self, input: InputDeleteUser):
        return await self.delete_user_use_case.execute(input.id)

    async def update_user(self, input: InputUpdateUser):
        user = await self.repository.get_by_id(input.id)
        if not user:
            raise UserNotFoundError
        request = UserInput(
            id=str(user.id),
            email=input.email if input.email else user.email,
            password=input.password if input.password else user.password,
            name=input.name if input.name else user.name,
            role=input.role.value if input.role else user.role.value,
            status=input.status.value if input.status else user.status.value,
        )

        return await self.update_user_use_case.execute(request)

    async def get_user_by_id(self, id: str):
        return await self.get_user_by_id_use_case.execute(id)

    async def get_user_by_email(self, email: str):
        return await self.get_user_by_email_use_case.execute(email)
