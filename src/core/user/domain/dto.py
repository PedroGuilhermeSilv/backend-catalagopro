from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict


class UserOutput(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    id: uuid.UUID
    store_slug: Optional[str] = None
    role: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class UserInput(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    password: str
    store_slug: Optional[str] = None
    role: Optional[str] = None
    model_config = ConfigDict(extra="forbid")
