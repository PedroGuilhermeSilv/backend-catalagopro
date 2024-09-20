import uuid

from ninja import Schema


class Error(Schema):
    message: str


class UserCreateDto(Schema):
    email: str
    password: str


class UserOutputDto(Schema):
    email: str
    id: uuid.UUID


response = {
    201: UserOutputDto,
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}
