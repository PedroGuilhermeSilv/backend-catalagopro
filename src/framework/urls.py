
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from src.core.externals.shopee.infra.api.controllers import router as router_shopee

api = NinjaAPI(urls_namespace="api-1.0.0")
api.add_router("/shopee", router_shopee)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
