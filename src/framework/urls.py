from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from src.core.user.infra.django.user.application.controllers.create_user import (
    router as create_user_router,
)

api = NinjaAPI(urls_namespace="api-1.0.0")

api.add_router("/user", create_user_router)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
