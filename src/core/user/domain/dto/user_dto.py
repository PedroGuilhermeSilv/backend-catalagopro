import uuid

from pydantic import BaseModel


class UserOutput(BaseModel):
    password: str
    email: str
    id: uuid.UUID


class UserInput(BaseModel):
    id: uuid.UUID
    email: str
    password: str
