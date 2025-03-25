from datetime import date

from src.core.shared.enums import Status
from src.core.shared.model import Model
from src.core.store.domain.enums import BusinessHour


class StoreListDto(Model):
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
