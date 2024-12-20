from ninja import Schema


class Error(Schema):
    message: str


class LoginInputDto(Schema):
    email: str
    password: str

class InputRefreshTokenDto(Schema):
    token: str

class LoginOutputDto(Schema):
    refresh_token: str
    token: str
    exp: int


response = {
    200: LoginOutputDto,
    403: Error,
    404: Error,
    500: Error,
}
