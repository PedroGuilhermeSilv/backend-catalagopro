from pydantic import BaseModel


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
