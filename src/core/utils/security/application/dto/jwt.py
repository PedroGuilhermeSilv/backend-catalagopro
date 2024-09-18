from dataclasses import dataclass


@dataclass
class JwtDto:
    token: str
    exp: str


@dataclass
class InputAuthUserDto:
    email: str
    password: str
