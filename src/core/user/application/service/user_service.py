from core.user.application.use_case.create_user import CreateUser
from core.user.application.service.user_dto import InputServiceCreateUser
from core.user.domain.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.create_user_use_case = CreateUser(self.repository)

    def create_user(self, input: InputServiceCreateUser):
        return self.create_user_use_case.execute(input)
