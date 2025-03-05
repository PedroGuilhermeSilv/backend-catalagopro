from ninja import Router
from src.core.user.infra.api.controllers.create_user import create
from src.core.user.infra.api.controllers.list_users import list
from src.core.user.infra.api.controllers.dtos import (
    response_user_create,
    response_user_list,
)

router = Router(tags=["User"])

router.add_api_operation("/", ["POST"], create, response=response_user_create)
router.add_api_operation("/", ["GET"], list, response=response_user_list)
