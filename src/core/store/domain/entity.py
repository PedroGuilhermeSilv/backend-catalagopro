import uuid
from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional
from uuid import UUID
from src.core.utils.regex import remove_accents_and_convert_to_slug
from src.core.store.domain.exceptions import InvalidSlugError
from src.core.utils.date import BusinessHour


class Store(BaseModel):
    name: str
    owner_id: str
    logo_url: str
    description: str
    address: str
    whatsapp: str
    business_hours: list[BusinessHour]
    slug: Optional[str] = None
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: date = Field(default_factory=date.today)
    updated_at: date = Field(default_factory=date.today)

    @model_validator(mode="after")
    def generate_slug(self):
        if self.slug is None and self.name:
            self.slug = remove_accents_and_convert_to_slug(self.name)
        return self

    @model_validator(mode="before")
    def validate_slug(self):
        if not self.get("slug") and not self.get("name"):
            raise InvalidSlugError()
        return self

    def model_dump(self, **kwargs):
        """
        Sobrescreve o método model_dump para formatar os dados corretamente
        """
        data = super().model_dump(**kwargs)
        if "business_hours" in data:
            data["business_hours"] = [hour.model_dump() for hour in self.business_hours]
        if "id" in data:
            data["id"] = str(data["id"])
        return data
