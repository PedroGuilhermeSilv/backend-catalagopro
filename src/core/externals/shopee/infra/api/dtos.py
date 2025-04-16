
from ninja import Schema


class Error(Schema):
    message: str


response = {
    404: Error,
    409: Error,
    400: Error,
    500: Error,
    422: Error,
}


class ProductOutput(Schema):
    item_id: int
    product_name: str
    price_min: str
    price_max: str
    commission_rate: str
    sales: int
    rating_star: str
    image_url: str
    product_link: str
    offer_link: str
    shop_name: str
    shop_id: int



class ListProductsOutput(Schema):
    data: list[ProductOutput]



class ProductAffiliateInput(Schema):
    product_url: str


class ProductAffiliateOutput(Schema):
    image_url: str
    product_name: str
    price_min: float
    price_max: float
    shop_name: str
    shop_id: int
    item_id: int
    affiliate_link: str
    description: str



response_list_products = response.copy()
response_list_products[200] =  ListProductsOutput


response_create_link_affiliate = response.copy()
response_create_link_affiliate[201] = ProductAffiliateOutput