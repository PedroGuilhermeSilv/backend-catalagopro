from dataclasses import dataclass


@dataclass
class ProductAffiliateOutput:
    image_url: str
    product_name: str
    price_min: float
    price_max: float
    shop_name: str
    shop_id: int
    item_id: int
    affiliate_link: str
    description: str

