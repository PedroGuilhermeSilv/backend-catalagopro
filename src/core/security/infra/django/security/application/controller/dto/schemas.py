from ninja import Schema


class Error(Schema):
    message: str


class LoginInputDto(Schema):
    email: str
    password: str


class LoginOutputDto(Schema):
    token: str
    exp: int


response = {
    200: LoginOutputDto,
    403: Error,
    404: Error,
    400: Error,
    500: Error,
    422: Error,
}
