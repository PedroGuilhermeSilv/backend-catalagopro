import uuid
from dataclasses import field
from enum import Enum
from typing import Self

from email_validator import validate_email
from pydantic import ConfigDict, field_validator, model_validator

from src.core.shared.enums import Status
from src.core.shared.hash import get_password_hash
from src.core.shared.model import Model
from src.core.user.domain.exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUserError,
)

LENGTH_PASSWORD = 8


class UserRole(Enum):
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    EMPLOYEE = "EMPLOYEE"

    @classmethod
    def from_value(cls, value):
        if not value:
            return None
        for item in cls:
            if item.value == value:
                return item
        return None

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class User(Model):
    name: str
    email: str
    password: str
    status: Status
    role: UserRole | None = None
    store_slug: str | None = None
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

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v is None:
            return None
        if isinstance(v, UserRole):
            return v
        if isinstance(v, str):
            try:
                return UserRole[v]
            except KeyError:
                try:
                    return UserRole(v)
                except ValueError:
                    return v
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if isinstance(v, Status):
            return v
        if isinstance(v, str):
            try:
                return Status[v]
            except KeyError:
                try:
                    return Status(v)
                except ValueError:
                    return v
        return v

    def __str__(self):
        return f"User: {self.email}, id: {self.id}"

    def __repr__(self):
        return f"User: {self.email}, id: {self.id}"

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.role and hasattr(self.role, "value"):
            data["role"] = self.role.value
        if self.status and hasattr(self.status, "value"):
            data["status"] = self.status.value
        return data

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=False,
    )
