from src.core.user.application.service.dto import InputDeleteUser
from src.core.user.application.service.user_service import UserService
from src.core.user.infra.api.controllers.dtos import (
    UserDeleteOutputDto,
)
from src.core.user.infra.database.repository import (
    DjangoUserRepository,
)


async def delete(request, id: str):
    try:
        service = UserService(repository=DjangoUserRepository())
        await service.delete_user(
            input=InputDeleteUser(id=id),
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 204, UserDeleteOutputDto(message="User deleted successfully")
