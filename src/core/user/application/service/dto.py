import uuid

from pydantic import field_validator

from src.core.shared.enums import Status
from src.core.shared.model import Model
from src.core.user.domain.entity import UserRole


class ModelValidator(Model):
    @field_validator("role", check_fields=False)
    @classmethod
    def validate_role(cls, v):
        if isinstance(v, UserRole):
            return v
        if isinstance(v, str):
            try:
                return UserRole[v]
            except KeyError:
                try:
                    return UserRole(v)
                except ValueError:
                    error_message = f"Invalid role value: {v}"
                    raise ValueError(error_message)
        error_type_message = f"Invalid role type: {type(v)}"
        raise ValueError(error_type_message)

    @field_validator("status", check_fields=False)
    @classmethod
    def validate_status(cls, v):
        if isinstance(v, Status):
            return v
        if isinstance(v, str):
            try:
                return Status[v]
            except KeyError:
                try:
                    return Status(v)
                except ValueError:
                    error_message = f"Invalid status value: {v}"
                    raise ValueError(error_message)
        error_type_message = f"Invalid status type: {type(v)}"
        raise ValueError(error_type_message)


class InputServiceCreateUser(Model):
    email: str
    password: str
    name: str
    role: UserRole
    status: Status
    store_slug: str | None = None


class OutputServiceCreateUser(Model):
    email: str
    id: str
    name: str
    store_slug: str | None = None
    role: UserRole
    status: Status


class InputCreateUser(ModelValidator):
    role: UserRole
    email: str
    password: str
    name: str
    status: Status
    store_slug: str | None = None


class OutputCreateUser(ModelValidator):
    email: str
    id: uuid.UUID
    role: UserRole
    store_slug: str | None = None
    name: str
    status: Status


class InputUpdateUser(ModelValidator):
    id: str
    email: str | None = None
    password: str | None = None
    name: str | None = None
    role: UserRole | None = None
    status: Status | None = None
    store_slug: str | None = None


class InputDeleteUser(Model):
    id: str
