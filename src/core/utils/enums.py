from enum import Enum


class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    @classmethod
    def from_value(cls, value):
        if not value:
            return None
        for item in cls:
            if item.value == value:
                return item
        return None
