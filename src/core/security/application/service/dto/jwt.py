from src.core.utils.model import Model


class JwtOutPutDto(Model):
    token: str
    refresh_token: str
    exp: int


class InputAuthUserDto(Model):
    email: str
    password: str


class InputRefreshToken(Model):
    refresh_token: str
