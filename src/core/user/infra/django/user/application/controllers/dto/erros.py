import uuid

from ninja import Schema


class Error(Schema):
    message: str


class UserOutputDto(Schema):
    email: str
    password: str


class UserCreateDto(Schema):
    email: str
    id: uuid.UUID
