from datetime import date

from src.core.store.domain.entity import BusinessHour, StoreStatus
from src.core.utils.model import Model


class StoreListDto(Model):
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
    business_hours: list[BusinessHour]
    owner_id: str
