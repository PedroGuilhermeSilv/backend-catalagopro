from core.user.infra.api.controllers.dtos import (
    UserUpdateInputDto,
)
from src.core.user.application.service.dto import InputUpdateUser
from src.core.user.application.service.user_service import UserService
from src.core.user.infra.database.repository import (
    DjangoUserRepository,
)


async def update(request, id: str, user: UserUpdateInputDto):
    try:
        service = UserService(repository=DjangoUserRepository())
        response = await service.update_user(
            input=InputUpdateUser(
                **{
                    **user.model_dump(),
                    "id": id,
                    "role": user.role.value,
                    "status": user.status.value,
                },
            ),
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}

    response_dict = response.model_dump()
    response_dict["id"] = str(response_dict["id"])

    return 200, response_dict
