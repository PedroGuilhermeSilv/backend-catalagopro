from typing import Any, Union
from ninja.security import HttpBearer
from src.core.utils.token import verify_token
from django.conf import settings
from ninja.errors import HttpError
from django.http import HttpRequest


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Any:
        if settings.DEBUG:
            return True
        payload = verify_token(token)
        return payload


class AuthBearerTenant(HttpBearer):
    def authenticate(self, request, token: str) -> Any:
        # if settings.DEBUG:
        #     return True
        payload = verify_token(token)
        tenent = self.get_tenant(request)
        role = payload.get("role")

        is_admin = role and role == "ADMIN"
        if is_admin:
            return payload
        if payload["tenant"] not in tenent:
            raise HttpError(400, f"Tenant inválido ou não especificado: {payload}")
        return payload

    def get_tenant(self, request: HttpRequest) -> Union[str, None]:
        return request.headers.get("X-Tenant-ID")
