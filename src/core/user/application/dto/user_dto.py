import uuid

from pydantic import BaseModel, ConfigDict


class InputCreateUser(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


class OutputCreateUser(BaseModel):
    email: str
    id: uuid.UUID
    model_config = ConfigDict(extra="forbid")
