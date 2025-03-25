import uuid

from pydantic import ConfigDict, field_validator

from src.core.shared.enums import Status
from src.core.shared.model import Model
from src.core.user.domain.entity import UserRole


class UserOutput(Model):
    name: str
    email: str
    id: uuid.UUID
    status: Status
    role: UserRole
    password: str | None = None
    store_slug: str | None = None
    model_config = ConfigDict(extra="forbid")

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

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.role and hasattr(self.role, "value"):
            data["role"] = self.role.value
        if self.status and hasattr(self.status, "value"):
            data["status"] = self.status.value
        return data


class UserInput(Model):
    id: uuid.UUID
    email: str
    name: str
    password: str
    status: Status
    store_slug: str | None = None
    role: UserRole | None = None
    model_config = ConfigDict(extra="forbid")

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

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        if self.role and hasattr(self.role, "value"):
            data["role"] = self.role.value
        if self.status and hasattr(self.status, "value"):
            data["status"] = self.status.value
        return data
