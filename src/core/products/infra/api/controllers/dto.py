from ninja import Schema


class Error(Schema):
    message: str


class CategoryInputDto(Schema):
    name: str
    store_slug: str


class CategoryOutputDto(Schema):
    id: str
    name: str
    store_id: str


class CategoryListOutputDto(Schema):
    data: list[CategoryOutputDto]


class SizeInputDto(Schema):
    name: str
    store_slug: str


class SizeOutputDto(Schema):
    id: str
    name: str
    store_id: str


class SizeListOutputDto(Schema):
    data: list[SizeOutputDto]


response = {
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}


response_category_create = response.copy()
response_category_create[201] = CategoryOutputDto

response_category_list = response.copy()
response_category_list[200] = CategoryListOutputDto


response_size_create = response.copy()
response_size_create[201] = SizeOutputDto

response_size_list = response.copy()
response_size_list[200] = SizeListOutputDto
