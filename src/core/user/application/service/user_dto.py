import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


class InputServiceCreateUser(BaseModel):
    email: str
    password: str
    name: str
    role: Optional[str] = None
    store_slug: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class OutputServiceCreateUser(BaseModel):
    email: str
    id: str
    name: str
    role: Optional[str] = None
    store_slug: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class InputCreateUser(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


class OutputCreateUser(BaseModel):
    email: str
    id: uuid.UUID
    role: Optional[str] = None
    store_slug: Optional[str] = None
    name: str
    model_config = ConfigDict(extra="forbid")
