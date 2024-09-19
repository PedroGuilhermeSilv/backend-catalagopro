from src.core.user.domain.dto.user_dto import UserInput, UserOutput
from src.core.user.domain.entity import User
from src.core.user.domain.repository.user_repository import UserRepository
from src.core.user.infra.django.user.models import User as UserModel


class DjangoUserRepository(UserRepository):
    def __init__(self):
        self.model = UserModel

    async def save(self, user: UserInput) -> UserOutput:
        try:
            user = User(
                id=user.id,
                password=user.password,
                email=user.email,
            )

            user_on_db = await self.model.objects.acreate(
                id=user.id,
                password=user.password,
                email=user.email,
            )
        except Exception as e:
            raise e

        return UserOutput(
            id=user_on_db.id,
            password=user_on_db.password,
            email=user_on_db.email,
        )

    async def get_by_email(self, email: str) -> UserOutput:
        try:
            user_on_db = await self.model.objects.aget(email=email)
        except Exception as e:
            raise e

        return UserOutput(
            id=user_on_db.id,
            password=user_on_db.password,
            email=user_on_db.email,
        )
