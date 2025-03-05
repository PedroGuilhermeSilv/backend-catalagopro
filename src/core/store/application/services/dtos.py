from pydantic import BaseModel
from typing import Optional
from src.core.utils.date import DayOfWeek
from src.core.utils.file import UploadedFile


class BusinessHourCreateDto(BaseModel):
    day: DayOfWeek
    open_hour: str
    close_hour: str


class InputServiceCreateStore(BaseModel):
    name: str
    email_owner: str
    description: str
    address: str
    whatsapp: str
    business_hours: list[BusinessHourCreateDto]
    image: Optional[UploadedFile] = None
