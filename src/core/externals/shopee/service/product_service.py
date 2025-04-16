

from src.core.externals.gemini.service.gemini_service import GeminiService
from src.core.externals.gemini.use_case.dto import InputCreateDescription
from src.core.externals.shopee.connection import Connection
from src.core.externals.shopee.service.dto import ProductAffiliateOutput
from src.core.externals.shopee.use_case.extract_product_info import UcExtractInfoProd
from src.core.externals.shopee.use_case.generate_affiliate_link import (
    UcGenerateAffiliateLink,
)
from src.core.externals.shopee.use_case.list_products import (
    ListProductsOutput,
    UCListProducts,
)

from google.genai import Client
class ProductServcie:
    def __init__(self, connection: Connection, client: Client) -> None:
        self.uc_list_products= UCListProducts(connection)
        self.uc_get_info_prod = UcExtractInfoProd(connection)
        self.uc_generate_affilieate_link = UcGenerateAffiliateLink(connection)
        self.gemini_service = GeminiService(client)

    def list_products(self)-> ListProductsOutput:
        return self.uc_list_products.execute()
    
    def create_link_affiliate_by_url(self,product_url: str)-> ProductAffiliateOutput:
        info_product = self.uc_get_info_prod.execute(product_url)
        if info_product:
            affiliate_link= self.uc_generate_affilieate_link.execute(product_url)
            description = self.gemini_service.create_description(
                InputCreateDescription(
                               image_url=info_product.image_url,
                product_name=info_product.product_name,
                price_min=info_product.price_min,
                price_max=info_product.price_max,
                shop_name=info_product.shop_name,
                offer_link=affiliate_link,
    
            ))
            return ProductAffiliateOutput(
                image_url=info_product.image_url,
                product_name=info_product.product_name,
                price_min=info_product.price_min,
                price_max=info_product.price_max,
                shop_name=info_product.shop_name,
                shop_id=info_product.shop_id,
                item_id=info_product.item_id,
                affiliate_link=affiliate_link,
                description=description
            )

