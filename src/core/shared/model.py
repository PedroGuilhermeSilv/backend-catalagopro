from enum import Enum

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        # Converter enums para seus valores string
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
        return data
