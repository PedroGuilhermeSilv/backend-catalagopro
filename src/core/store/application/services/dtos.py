from datetime import date

from src.core.store.domain.entity import StoreStatus
from src.core.utils.date import DayOfWeek
from src.core.utils.file import UploadedFile
from src.core.utils.model import Model


class BusinessHourCreateDto(Model):
    day: DayOfWeek
    open_hour: str
    close_hour: str


class InputServiceCreateStore(Model):
    name: str
    email_owner: str
    description: str
    address: str
    status: StoreStatus
    whatsapp: str
    business_hours: list[BusinessHourCreateDto]
    image: UploadedFile | None = None


class StoreDto(Model):
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
    business_hours: list[BusinessHourCreateDto]
    owner_id: str
    owner_name: str


class OutputServiceListStore(Model):
    data: list[StoreDto]
