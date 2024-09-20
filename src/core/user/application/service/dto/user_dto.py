from pydantic import BaseModel, ConfigDict


class InputServiceCreateUser(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


class OutputServiceCreateUser(BaseModel):
    email: str
    id: str

    model_config = ConfigDict(extra="forbid")
