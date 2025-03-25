from datetime import datetime
from typing import Any
import uuid
from pydantic import Field

from src.core.shared.model import Model


class Category(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str


class Size(Model):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str


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
    name: str
    description: str
    default_price: Price | None = None
    size_price: list[SizePrice] | None = None
    category: Category
    image: list[Image]
    created_at: datetime
    updated_at: datetime

    def model_post_init(self, __context: Any) -> None:
        self.validate()

    def validate(self):
        if self.default_price is None and self.size_price is None:
            raise ValueError("O produto deve ter pelo menos um preço")

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

        if self.size_price and size_id:
            for size_price in self.size_price:
                if size_price.size.id == size_id:
                    return size_price.price.value

        raise ValueError("Preço não encontrado para o tamanho especificado")
