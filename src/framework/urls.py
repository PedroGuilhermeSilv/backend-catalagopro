from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from core.security.infra.api.controller.dto import (
    router as login_router,
)

from src.core.store.infra.api.controllers.create_store import (
    router as store_router,
)
from src.core.user.infra.api.config import router as user_router

api = NinjaAPI(urls_namespace="api-1.0.0")

api.add_router("/user", user_router)
api.add_router("/auth", login_router)
api.add_router("/store", store_router)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
