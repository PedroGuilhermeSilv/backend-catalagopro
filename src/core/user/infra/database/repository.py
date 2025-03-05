from typing import Union
from src.core.user.domain.dto import UserInput, UserOutput
from src.core.user.domain.repository import UserRepository
from src.core.user.infra.database.models import User as UserModel
from src.core.store.infra.database.models import Store as StoreModel
from asgiref.sync import sync_to_async


class DjangoUserRepository(UserRepository):
    def __init__(self):
        self.model = UserModel
        self.store_model = StoreModel

    async def save(self, user: UserInput) -> UserOutput:
        try:
            user_on_db = await self.model.objects.acreate(
                id=user.id,
                password=user.password,
                name=user.name,
                email=user.email,
                role=user.role,
            )
        except Exception as e:
            raise e

        store = await self.store_model.objects.filter(owner_id=user_on_db.id).afirst()
        store_slug = store.slug if store else None

        return UserOutput(
            id=user_on_db.id,
            name=user_on_db.name,
            email=user_on_db.email,
            store_slug=store_slug,
            role=user_on_db.role,
            
        )

    async def get_by_email(self, email: str) -> UserOutput | None:
        if user_on_db := await self.model.objects.filter(email=email).afirst():
            store = await self.store_model.objects.filter(
                owner_id=user_on_db.id
            ).afirst()
            store_slug = store.slug if store else None

            return UserOutput(
                id=user_on_db.id,
                email=user_on_db.email,
                name=user_on_db.name,
                store_slug=store_slug,
                role=user_on_db.role,
                password=user_on_db.password,
            )
        return None

    async def list(self) -> Union[list[UserOutput], None]:
        users = await sync_to_async(list)(self.model.objects.all())
        return [
            UserOutput(
                name=user.name,
                email=user.email,
                role=user.role,
                id=user.id,
                store_slug=(
                    (
                        await self.store_model.objects.filter(owner_id=user.id).afirst()
                    ).slug
                    if await self.store_model.objects.filter(owner_id=user.id).afirst()
                    else None
                ),
            )
            for user in users
        ]
