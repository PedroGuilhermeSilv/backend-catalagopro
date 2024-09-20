from pydantic import BaseModel


class JwtDto(BaseModel):
    token: str
    exp: int


class InputAuthUserDto(BaseModel):
    email: str
    password: str
