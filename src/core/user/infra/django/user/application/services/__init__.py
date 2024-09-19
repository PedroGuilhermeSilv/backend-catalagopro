from ninja import Schema


class UserCreateDto(Schema):
    email: str
    password: str
