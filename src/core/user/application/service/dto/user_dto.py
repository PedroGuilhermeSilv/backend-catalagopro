from pydantic import BaseModel


class InputServiceCreateUser(BaseModel):
    email: str
    password: str


class OutputServiceCreateUser(BaseModel):
    email: str
    id: str
