from core.user.application.use_case.create_user import (
    InputServiceCreateUser,
)
from core.user.infra.api.controllers.dtos import (
    UserCreateDto,
)
from src.core.user.application.service.user_service import UserService
from src.core.user.infra.database.repository import (
    DjangoUserRepository,
)


async def create(request, user: UserCreateDto):
    try:
        service = UserService(repository=DjangoUserRepository())
        response = await service.create_user(
            input=InputServiceCreateUser(
                **{
                    **user.model_dump(),
                    "role": user.role.value,
                    "status": user.status.value,
                },
            ),
        )
    except Exception as e:
        return e.status_code, {"message": str(e.msg)}

    # Converter para dicionário e formatar valores
    response_dict = response.model_dump()
    response_dict["id"] = str(response_dict["id"])

    return 201, response_dict
