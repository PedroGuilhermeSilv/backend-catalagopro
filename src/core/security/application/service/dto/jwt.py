from pydantic import BaseModel


class JwtOutPutDto(BaseModel):
    token: str
    refresh_token: str
    exp: int


class InputAuthUserDto(BaseModel):
    email: str
    password: str


class InputRefreshToken(BaseModel):
    refresh_token: str
