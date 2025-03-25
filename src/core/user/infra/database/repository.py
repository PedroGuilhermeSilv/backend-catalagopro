from asgiref.sync import sync_to_async

from src.core.store.infra.database.models import Store as StoreModel
from src.core.user.domain.dto import UserInput, UserOutput
from src.core.user.domain.exceptions import UserNotFoundError
from src.core.user.infra.database.models import User as UserModel
from src.core.user.infra.interfaces.repository import UserRepository


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
                role=user.role.value,
                status=user.status.value,
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
            status=user_on_db.status,
        )

    async def get_by_email(self, email: str) -> UserOutput | None:
        if user_on_db := await self.model.objects.filter(email=email).afirst():
            store = await self.store_model.objects.filter(
                owner_id=user_on_db.id,
            ).afirst()
            store_slug = store.slug if store else None

            return UserOutput(
                id=user_on_db.id,
                email=user_on_db.email,
                name=user_on_db.name,
                store_slug=store_slug,
                role=user_on_db.role,
                password=user_on_db.password,
                status=user_on_db.status,
            )
        return None

    async def get_by_id(self, id: str) -> UserOutput | None:
        if user_on_db := await self.model.objects.filter(id=id).afirst():
            store = await self.store_model.objects.filter(
                owner_id=user_on_db.id,
            ).afirst()
            store_slug = store.slug if store else None

            return UserOutput(
                id=user_on_db.id,
                email=user_on_db.email,
                name=user_on_db.name,
                store_slug=store_slug,
                role=user_on_db.role,
                password=user_on_db.password,
                status=user_on_db.status,
            )
        return None

    async def list(self) -> list[UserOutput] | None:
        users = await sync_to_async(list)(self.model.objects.all())
        return [
            UserOutput(
                name=user.name,
                email=user.email,
                role=user.role,
                status=user.status,
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

    async def delete(self, id: str) -> None:
        user = await self.model.objects.filter(id=id).afirst()
        if not user:
            raise UserNotFoundError
        await user.adelete()

    async def update(self, user: UserInput) -> UserOutput:
        user_on_db = await self.model.objects.filter(id=user.id).afirst()
        if not user_on_db:
            raise UserNotFoundError
        user_on_db.email = user.email
        user_on_db.name = user.name
        user_on_db.role = user.role.value
        user_on_db.status = user.status.value
        user_on_db.store_slug = user.store_slug
        user_on_db.password = user.password
        await user_on_db.asave()

        return UserOutput(
            id=user_on_db.id,
            email=user_on_db.email,
            name=user_on_db.name,
            role=user_on_db.role,
            status=user_on_db.status,
            store_slug=user_on_db.store_slug,
        )
