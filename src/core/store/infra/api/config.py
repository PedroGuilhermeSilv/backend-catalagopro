from ninja import Router
from src.core.security.infra.api.controller.auth import AuthBearerTenant
from src.core.store.infra.api.controllers.dtos import (
    response_store_create,
    response_store_list,
)

from core.store.infra.api.controllers.create_store import create
from core.store.infra.api.controllers.list_store import list

router = Router(tags=["Store"])

router.add_api_operation(
    "/",
    ["POST"],
    create,
    response=response_store_create,
    auth=AuthBearerTenant(),
)
router.add_api_operation(
    "/",
    ["GET"],
    list,
    response=response_store_list,
    auth=AuthBearerTenant(),
)
