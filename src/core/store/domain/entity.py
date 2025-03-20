import re
import unicodedata
import uuid
from datetime import date
from enum import Enum

from pydantic import Field, model_validator
from src.core.store.domain.exceptions import InvalidSlugError
from src.core.utils.date import BusinessHour
from src.core.utils.model import Model


class StoreStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class Store(Model):
    name: str
    owner_id: str
    logo_url: str
    description: str
    address: str
    whatsapp: str
    business_hours: list[BusinessHour]
    slug: str | None = None
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: date = Field(default_factory=date.today)
    updated_at: date = Field(default_factory=date.today)
    status: StoreStatus = StoreStatus.ACTIVE

    @model_validator(mode="after")
    def generate_slug(self):
        if self.slug is None and self.name:
            self.slug = self.remove_accents_and_convert_to_slug(self.name)
        return self

    @model_validator(mode="before")
    def validate_slug(self):
        if not self.get("slug") and not self.get("name"):
            raise InvalidSlugError
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

    def remove_accents_and_convert_to_slug(self, text: str) -> str:
        """
        Converte um texto para slug:
        - Remove acentos
        - Converte para minúsculo
        - Remove caracteres especiais
        - Substitui espaços por hífens
        - Remove hífens duplicados
        """

        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode("utf-8")
        )

        text = text.lower()

        text = re.sub(r"[^\w\s-]", " ", text)

        text = re.sub(r"[\s_]+", "-", text)

        return text.strip("-")
