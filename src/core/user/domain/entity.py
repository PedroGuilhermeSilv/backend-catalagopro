import uuid
from dataclasses import field
from typing import Self

from email_validator import validate_email
from pydantic import BaseModel, ConfigDict, model_validator

from src.core.user.domain.exceptions.user_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUserError,
)
from src.core.utils.hash import get_password_hash

LENGTH_PASSWORD = 8


class User(BaseModel):
    email: str
    password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @model_validator(mode="before")
    @classmethod
    def check_based_info(cls, data: dict) -> dict:
        if not data.get("email"):
            raise InvalidUserError
        if not data.get("password"):
            raise InvalidUserError
        if len(data.get("password")) < LENGTH_PASSWORD:
            raise InvalidPasswordError
        try:
            validate_email(data.get("email"))
        except Exception as e:
            raise InvalidEmailError from e
        return data

    @model_validator(mode="after")
    def hash_password(self) -> Self:
        self.password = get_password_hash(self.password)
        return self

    def __str__(self):
        return f"User: {self.email}, id: {self.id}"

    def __repr__(self):
        return f"User: {self.email}, id: {self.id}"

    model_config = ConfigDict(extra="forbid")
