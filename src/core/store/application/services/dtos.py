from datetime import date

from src.core.shared.enums import Status
from src.core.shared.file import UploadedFile
from src.core.shared.model import Model
from src.core.store.domain.enums import DayOfWeek


class BusinessHour(Model):
    day: DayOfWeek
    open_hour: str
    close_hour: str


class InputServiceCreateStore(Model):
    name: str
    email_owner: str
    description: str
    address: str
    status: Status
    whatsapp: str
    business_hours: list[BusinessHour]
    image: UploadedFile | None = None


class InputServiceUpdateStore(Model):
    store_id: str
    name: str | None = None
    slug: str | None = None
    image: UploadedFile | None = None
    description: str | None = None
    address: str | None = None
    whatsapp: str | None = None
    business_hours: list[BusinessHour] | None = None
    status: Status | None = None
    owner_id: str | None = None


class StoreDto(Model):
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
    business_hours: list[BusinessHour]
    owner_id: str
    owner_name: str


class OutputServiceListStore(Model):
    data: list[StoreDto]
