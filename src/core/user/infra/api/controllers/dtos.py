import uuid
from typing import Optional
from ninja import Schema


class Error(Schema):
    message: str


class UserCreateDto(Schema):
    email: str
    password: str
    name: str
    role: Optional[str] = None


class UserOutputDto(Schema):
    email: str
    role: Optional[str] = None
    name: str
    store_slug: Optional[str] = None
    id: uuid.UUID


class UserListOutputDto(Schema):
    data: list[UserOutputDto]


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
