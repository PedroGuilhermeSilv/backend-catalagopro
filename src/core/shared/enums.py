from enum import Enum


class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    def __str__(self) -> str:
        return self.value
