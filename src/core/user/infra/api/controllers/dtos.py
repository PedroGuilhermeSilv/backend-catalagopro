import uuid

from ninja import Schema
from pydantic import field_validator

from core.utils.enums import Status
from src.core.user.domain.entity import UserRole


class Error(Schema):
    message: str


class DeleteUserDto(Schema):
    id: str


class UserCreateDto(Schema):
    email: str
    password: str
    name: str
    role: UserRole | None = None
    status: Status

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return None
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

    @field_validator("status")
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


class UserOutputDto(Schema):
    email: str
    role: str
    name: str
    store_slug: str | None = None
    id: uuid.UUID
    status: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return None
        if isinstance(v, UserRole):
            return v.value
        if isinstance(v, str):
            return v
        error_type_message = f"Invalid role type: {type(v)}"
        raise ValueError(error_type_message)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if isinstance(v, Status):
            return v.value
        if isinstance(v, str):
            return v
        error_type_message = f"Invalid status type: {type(v)}"
        raise ValueError(error_type_message)


class UserListOutputDto(Schema):
    data: list[UserOutputDto]


class UserDeleteOutputDto(Schema):
    message: str


class UserUpdateInputDto(Schema):
    email: str
    role: UserRole | None = None
    name: str
    store_slug: str | None = None
    status: Status

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return None
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

    @field_validator("status")
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


class UserUpdateOutputDto(Schema):
    email: str
    role: str
    name: str
    store_slug: str | None = None
    status: str
    id: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return None
        if isinstance(v, UserRole):
            return v.value
        if isinstance(v, str):
            return v
        error_message = f"Invalid role type: {type(v)}"
        raise ValueError(error_message)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if isinstance(v, Status):
            return v.value
        if isinstance(v, str):
            return v
        error_message = f"Invalid status type: {type(v)}"
        raise ValueError(error_message)


response = {
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}

response_user_create = response.copy()
response_user_create[201] = UserOutputDto


response_user_list = response.copy()
response_user_list[200] = UserListOutputDto


response_user_delete = {
    204: UserDeleteOutputDto,
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}


response_user_update = response.copy()
response_user_update[200] = UserUpdateOutputDto
