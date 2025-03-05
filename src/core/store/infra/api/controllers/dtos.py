from ninja import Schema
from src.core.utils.date import DayOfWeek


class Error(Schema):
    message: str


class BusinessHourCreateDto(Schema):
    day: DayOfWeek
    open_hour: str
    close_hour: str


class StoreCreateOutputDto(Schema):
    id: str
    name: str
    owner_id: str
    description: str
    address: str
    whatsapp: str
    business_hours: list[BusinessHourCreateDto]


response = {
    201: StoreCreateOutputDto,
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}
