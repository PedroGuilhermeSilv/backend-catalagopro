import uuid
from datetime import datetime
from typing import Any

from pydantic import Field

from src.core.shared.model import Model


class Category(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    store_id: str


class Size(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    store_id: str


class Price(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    value: int


class Image(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str


class SizePrice(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    size: Size
    price: Price


class Product(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    store_id: str
    name: str
    description: str
    default_price: Price | None = None
    size_price: list[SizePrice] | None = None
    category: Category
    image: list[Image]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def model_post_init(self, __context: Any) -> None:  # noqa: PYI063
        self.validate()

    def validate(self):
        if self.default_price is None and self.size_price is None:
            msg = "O produto deve ter pelo menos um preço"
            raise ValueError(msg)

    @property
    def has_sizes(self) -> bool:
        """Verifica se o produto tem variações de tamanho"""
        return bool(self.size_price)

    def get_price(self, size_id: str | None = None) -> float:
        """
        Retorna o preço do produto
        Se size_id for fornecido, retorna o preço do tamanho específico
        Caso contrário, retorna o preço default
        """
        if not size_id and self.default_price:
            return self.default_price.value

        if size_id and self.size_price is not None:
            for size_price in self.size_price:
                if size_price.size.id == size_id:
                    return size_price.price.value
        msg = "Preço não encontrado para o tamanho especificado"
        raise ValueError(msg)
