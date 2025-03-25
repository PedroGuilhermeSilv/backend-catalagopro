from enum import Enum
from src.core.shared.model import Model
from datetime import time


class DayOfWeek(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def from_int(cls, value: int) -> "DayOfWeek":
        for day in cls:
            if day.value == value:
                return day
        error_message = f"Invalid day value: {value}"
        raise ValueError(error_message)

    def __str__(self) -> str:
        return self.name.title()


class BusinessHour(Model):
    day: DayOfWeek
    open_hour: time
    close_hour: time

    @property
    def formatted_open_hour(self) -> str:
        """Retorna o horário de abertura formatado"""
        return self.open_hour.strftime("%H:%M")

    @property
    def formatted_close_hour(self) -> str:
        """Retorna o horário de fechamento formatado"""
        return self.close_hour.strftime("%H:%M")

    @classmethod
    def create(cls, day: int, open_hour: str, close_hour: str) -> "BusinessHour":
        """
        Cria um horário de funcionamento a partir de valores básicos

        Args:
            day: número do dia (1-7)
            open_hour: horário de abertura no formato "HH:MM"
            close_hour: horário de fechamento no formato "HH:MM"
        """
        return cls(
            day=DayOfWeek.from_int(day),
            open_hour=time.fromisoformat(open_hour),
            close_hour=time.fromisoformat(close_hour),
        )

    def model_dump(self, **kwargs):
        """Sobrescreve o método model_dump para formatar os horários"""
        data = super().model_dump(**kwargs)
        if "open_hour" in data and data["open_hour"] is not None:
            data["open_hour"] = self.formatted_open_hour
        if "close_hour" in data and data["close_hour"] is not None:
            data["close_hour"] = self.formatted_close_hour
        if "day" in data and data["day"] is not None:
            data["day"] = self.day.value
        return data

    def model_dump_json(self, **kwargs):
        data = super().model_dump(**kwargs)
        if "open_hour" in data and data["open_hour"] is not None:
            data["open_hour"] = self.formatted_open_hour
        if "close_hour" in data and data["close_hour"] is not None:
            data["close_hour"] = self.formatted_close_hour
        if "day" in data and data["day"] is not None:
            data["day"] = self.day.value
        return data

    def __str__(self) -> str:
        return f"{self.day} - {self.formatted_open_hour} - {self.formatted_close_hour}"
