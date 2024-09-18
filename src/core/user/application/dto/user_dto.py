import uuid

from pydantic import BaseModel


class InputCreateUser(BaseModel):
    email: str
    password: str


class OutputCreateUser(BaseModel):
    email: str
    id: uuid.UUID
