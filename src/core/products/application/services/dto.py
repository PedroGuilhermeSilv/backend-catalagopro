from typing import Any

from pydantic import BaseModel

from src.core.shared.file import UploadedFile


class CategoryInputDto(BaseModel):
    name: str
    store_slug: str


class CategoryOutputDto(BaseModel):
    id: str
    name: str
    store_id: str


class CategoryListOutputDto(BaseModel):
    data: list[CategoryOutputDto]


class SizeInputDto(BaseModel):
    name: str
    store_slug: str


class SizeOutputDto(BaseModel):
    id: str
    name: str
    store_id: str


class SizeListOutputDto(BaseModel):
    data: list[SizeOutputDto]


class SizePriceInputDto(BaseModel):
    size_id: str
    price: float


class ProductInputDto(BaseModel):
    name: str
    description: str
    category_id: str
    default_price: float | None = None
    sizes: list[SizePriceInputDto] | None = None
    image: list[UploadedFile]

    def validate(self):
        if self.sizes is None and self.default_price is None:
            msg = "O produto deve ter pelo menos um tamanho ou um preço"
            raise ValueError(msg)

    def model_post_init(self, __context: Any) -> None:  # noqa: PYI063
        self.validate()


class ProductOutputDto(BaseModel):
    id: str
    name: str
    description: str
    category_id: str
    size_id: str
    price: float
    image: list[str]
