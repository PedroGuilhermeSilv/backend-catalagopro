from pydantic import BaseModel
class InputCreateDescription(BaseModel):
      product_name: str
      price_min: float
      price_max: float
      image_url: str
      offer_link: str
      shop_name: str