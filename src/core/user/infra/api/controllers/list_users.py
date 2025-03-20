from src.core.user.application.service.user_service import UserService
from src.core.user.infra.api.controllers.dtos import (
    UserListOutputDto,
    UserOutputDto,
)
from src.core.user.infra.database.repository import (
    DjangoUserRepository,
)


async def list(request):
    try:
        service = UserService(repository=DjangoUserRepository())
        result = await service.list_users()
        result = UserListOutputDto(
            data=[UserOutputDto(**user.model_dump()) for user in result],
        )

    except Exception as e:
        return e.status_code, {"message": str(e.msg)}
    return 200, result
