from src.core.user.application.use_case.create_user import CreateUser
from src.core.user.application.service.user_dto import InputServiceCreateUser
from src.core.user.application.use_case.list_users import UseCaseListUsers
from src.core.user.domain.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.create_user_use_case = CreateUser(self.repository)
        self.list_users_use_case = UseCaseListUsers(self.repository)

    def create_user(self, input: InputServiceCreateUser):
        return self.create_user_use_case.execute(input)

    def list_users(self):
        return self.list_users_use_case.execute()
