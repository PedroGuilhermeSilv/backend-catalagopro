import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.core.externals.shopee.auth import ShopeeBaseAuth


@dataclass
class ProductInfo:
    image_url: str
    product_name: str
    price_min: float
    price_max: float
    shop_name: str
    shop_id: int
    item_id: int


class UcExtractInfoProd(ShopeeBaseAuth):

    def get_product_details(self, item_id: int, shop_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a product."""
        query = f'''query{{
            productOfferV2(itemId:{item_id}, shopId:{shop_id}){{
                nodes{{
                    itemId
                    productName
                    priceMin
                    priceMax
                    imageUrl
                    productLink
                    offerLink
                    shopName
                    shopId
                }}
            }}
        }}'''
        
        response = self._make_request(query)
        
        if response.get("errors"):
            print("Erro na resposta:", response.get("errors"))
            return None
            
        nodes = response.get("data", {}).get("productOfferV2", {}).get("nodes", [])
        if not nodes:
            print("Nenhum produto encontrado")
            return None
            
        return nodes[0]

    def execute(self, product_url: str) -> Optional[ProductInfo]:
        """
        Extract product information from a Shopee product link.
        
        Args:
            product_url (str): The Shopee product URL
            
        Returns:
            Optional[ProductInfo]: Product information including image URL, product name, prices, etc.
        """
        try:
            # Extract item_id and shop_id from URL
            match = re.search(r'i\.(\d+)\.(\d+)', product_url)
            if not match:
                print("Invalid Shopee URL format")
                return None
                
            shop_id = int(match.group(1))
            item_id = int(match.group(2))
            
            # Get product details
            item = self.get_product_details(item_id, shop_id)
            if not item:
                return None
            
            # Get prices directly from the API response
            try:
                price_min = float(item.get('priceMin', '0'))
                price_max = float(item.get('priceMax', '0'))
            except (ValueError, TypeError) as e:
                print(f"Error converting prices to numbers: {e}")
                price_min = price_max = 0
            
            return ProductInfo(
                image_url=item.get('imageUrl'),
                product_name=item.get('productName', "Produto Shopee"),
                price_min=price_min,
                price_max=price_max,
                shop_name=item.get('shopName', ""),
                shop_id=shop_id,
                item_id=item_id
            )
            
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None


