import uuid

from pydantic import BaseModel, ConfigDict


class UserOutput(BaseModel):
    password: str
    email: str
    id: uuid.UUID

    model_config = ConfigDict(extra="forbid")


class UserInput(BaseModel):
    id: uuid.UUID
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")
