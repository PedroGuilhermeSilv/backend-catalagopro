from ninja import Router

from src.core.products.infra.api.controllers.create_category import create_category
from src.core.products.infra.api.controllers.create_size import create_size
from src.core.products.infra.api.controllers.dto import (
    response_category_create,
    response_category_list,
    response_size_create,
    response_size_list,
)
from src.core.products.infra.api.controllers.list_categories import list_categories
from src.core.products.infra.api.controllers.list_size import list_sizes
from src.core.security.infra.api.controller.auth import AuthBearerTenant

router_category = Router(tags=["Category"])


router_category.add_api_operation(
    "/",
    ["POST"],
    create_category,
    response=response_category_create,
    auth=AuthBearerTenant(),
)

router_category.add_api_operation(
    "/{store_slug}",
    ["GET"],
    list_categories,
    response=response_category_list,
    auth=AuthBearerTenant(),
)


router_size = Router(tags=["Size"])

router_size.add_api_operation(
    "/",
    ["POST"],
    create_size,
    response=response_size_create,
    auth=AuthBearerTenant(),
)

router_size.add_api_operation(
    "/{store_slug}",
    ["GET"],
    list_sizes,
    response=response_size_list,
    auth=AuthBearerTenant(),
)
