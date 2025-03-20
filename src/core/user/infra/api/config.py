from ninja import Router

from src.core.security.infra.api.controller.auth import AuthBearerTenant
from src.core.user.infra.api.controllers.create_user import create
from src.core.user.infra.api.controllers.delete_user import delete
from src.core.user.infra.api.controllers.dtos import (
    response_user_create,
    response_user_delete,
    response_user_list,
    response_user_update,
)
from src.core.user.infra.api.controllers.list_users import list
from src.core.user.infra.api.controllers.update_user import update

router = Router(tags=["User"])

router.add_api_operation(
    "/",
    ["POST"],
    create,
    response=response_user_create,
    auth=AuthBearerTenant(),
)
router.add_api_operation(
    "/",
    ["GET"],
    list,
    response=response_user_list,
    auth=AuthBearerTenant(),
)
router.add_api_operation(
    "/{id}",
    ["DELETE"],
    delete,
    response=response_user_delete,
    auth=AuthBearerTenant(),
)
router.add_api_operation(
    "/{id}",
    ["PATCH"],
    update,
    response=response_user_update,
    auth=AuthBearerTenant(),
)
