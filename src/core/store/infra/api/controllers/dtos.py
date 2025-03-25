from datetime import date

from ninja import Schema
from src.core.shared.enums import Status
from src.core.store.domain.enums import DayOfWeek


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


class StoreUpdateDto(Schema):
    name: str | None = None
    slug: str | None = None
    logo_url: str | None = None
    description: str | None = None
    address: str | None = None
    whatsapp: str | None = None
    business_hours: list[BusinessHourCreateDto] | None = None
    status: Status | None = None
    owner_id: str | None = None


class StoreCreateOutputDto(Schema):
    id: str
    name: str
    owner_id: str
    description: str
    address: str
    whatsapp: str
    status: Status
    business_hours: list[BusinessHourCreateDto]


class StoreDto(Schema):
    id: str
    name: str
    slug: str
    created_at: date
    updated_at: date
    status: Status
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


response_store_update = response.copy()
response_store_update[201] = StoreUpdateDto


response_store_delete = response.copy()
response_store_delete[204] = None
