from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from core.security.infra.api.controller.dto import (
    router as login_router,
)
from src.core.user.infra.api.controllers.create_user import (
    router as create_user_router,
)

api = NinjaAPI(urls_namespace="api-1.0.0")

api.add_router("/user", create_user_router)
api.add_router("/auth", login_router)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
