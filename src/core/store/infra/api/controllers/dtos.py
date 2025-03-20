from datetime import date

from ninja import Schema
from src.core.store.domain.entity import StoreStatus
from src.core.utils.date import DayOfWeek


class Error(Schema):
    message: str


class BusinessHourCreateDto(Schema):
    day: DayOfWeek
    open_hour: str
    close_hour: str


class BusinessHourDto(Schema):
    day: int
    open_hour: str
    close_hour: str


class StoreCreateOutputDto(Schema):
    id: str
    name: str
    owner_id: str
    description: str
    address: str
    whatsapp: str
    status: StoreStatus
    business_hours: list[BusinessHourCreateDto]


class StoreDto(Schema):
    id: str
    name: str
    slug: str
    created_at: date
    updated_at: date
    status: StoreStatus
    logo_url: str
    description: str
    address: str
    whatsapp: str
    business_hours: list[BusinessHourDto]
    owner_id: str
    owner_name: str


class StoreListOutputDto(Schema):
    data: list[StoreDto]


response = {
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}


response_store_create = response.copy()
response_store_create[201] = StoreCreateOutputDto


response_store_list = response.copy()
response_store_list[200] = StoreListOutputDto
