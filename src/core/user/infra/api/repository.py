from src.core.user.domain.dto import UserInput, UserOutput
from src.core.user.domain.repository import UserRepository
from src.core.user.infra.api.models import User as UserModel


class DjangoUserRepository(UserRepository):
    def __init__(self):
        self.model = UserModel

    async def save(self, user: UserInput) -> UserOutput:
        try:
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

    async def get_by_email(self, email: str) -> UserOutput | None:
        if user_on_db := await self.model.objects.filter(email=email).afirst():
            return UserOutput(
                id=user_on_db.id,
                password=user_on_db.password,
                email=user_on_db.email,
            )
        return None
