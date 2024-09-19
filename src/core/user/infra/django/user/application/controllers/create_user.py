from ninja import Router
from src.core.user.application.service.create_user import CreateUser, UserInput
from src.core.user.infra.django.user.application.controllers import UserCreateDto
from src.core.user.infra.django.user.repositories.user_repository import (
    DjangoUserRepository,
)

router = Router()


@router.post("/")
def create(request, user: UserCreateDto):
    service = CreateUser(repository=DjangoUserRepository())
    response = service.execute(input=UserInput(**user.dict()))
    return {"msg": response}
