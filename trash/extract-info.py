import hashlib
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class ProductInfo:
    image_url: str
    affiliate_link: str
    sales_text: str
    price_min: float
    price_max: float


class UcExtractInfoProd:
    def __init__(self, app_id: str, secret: str):
        self.app_id = app_id
        self.secret = secret
        self.base_url = 'https://open-api.affiliate.shopee.com.br/graphql'

    def _generate_signature(self, timestamp: int, payload: str) -> str:
        """Generate SHA256 signature for API authentication."""
        factor = f"{self.app_id}{timestamp}{payload}{self.secret}"
        return hashlib.sha256(factor.encode()).hexdigest()

    def _make_request(self, query: str) -> Dict[str, Any]:
        """Make a request to the Shopee API."""
        timestamp = int(time.time())
        payload = json.dumps({"query": query})
        signature = self._generate_signature(timestamp, payload)
        
        headers = {
            'Authorization': f"SHA256 Credential={self.app_id}, Timestamp={timestamp}, Signature={signature}",
            'Content-Type': 'application/json'
        }
        
        response = requests.post(self.base_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()

    def generate_short_link(self, url: str) -> str:
        """Generate a short affiliate link for a product URL."""
        query = f'''mutation{{
            generateShortLink(input:{{
                originUrl:"{url}",
                subIds:["s1","s2","s3","s4","s5"]
            }}){{
                shortLink
            }}
        }}'''
        
        response = self._make_request(query)
        return response.get('data', {}).get('generateShortLink', {}).get('shortLink', url)

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

    def extract_product_info(self, product_url: str) -> Optional[ProductInfo]:
        """
        Extract product information from a Shopee product link.
        
        Args:
            product_url (str): The Shopee product URL
            
        Returns:
            Optional[ProductInfo]: Product information including image URL, affiliate link and sales text
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
                
            # Generate affiliate link
            short_link = self.generate_short_link(product_url)
            
            # Extract product information
            image_url = item.get('imageUrl')
            product_name = item.get('productName', "Produto Shopee")
            
            # Get prices directly from the API response
            try:
                price_min = float(item.get('priceMin', '0'))
                price_max = float(item.get('priceMax', '0'))
            except (ValueError, TypeError) as e:
                print(f"Error converting prices to numbers: {e}")
                price_min = price_max = 0
            
            # Format price for sales text
            if price_min == price_max:
                price_text = f"R$ {price_min:.2f}"
            else:
                price_text = f"R$ {price_min:.2f} - R$ {price_max:.2f}"
            
            # Create sales text
            sales_text = f"🔥 {product_name} por apenas {price_text}! 🛍️\n\nClique no link abaixo para aproveitar:\n{short_link}"
            
            return ProductInfo(
                image_url=image_url,
                affiliate_link=short_link,
                sales_text=sales_text,
                price_min=price_min,
                price_max=price_max
            )
            
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None


# Exemplo de uso
if __name__ == "__main__":
    # Credenciais
    app_id = "18365700060"
    secret = "K6R6PQPQCFQU2CST6B4QGJ6P6FPN4PYG"
    
    # Criar instância do serviço
    shopee_service = ShopeeService(app_id, secret)
    
    # URL de exemplo
    product_url = "https://shopee.com.br/Carga-Magn%C3%A9tica-%C3%80-Prova-De-Choque-P%C3%A1ra-Choques-Caso-De-Telefone-Compat%C3%ADvel-Para-Iphone-16-13-15-11-14-Quadro-Capa-Clara-i.1006215031.27026192846?sp_atk=bf8384c2-9541-4f4c-92be-8af855f5f571&xptdk=bf8384c2-9541-4f4c-92be-8af855f5f571"
    
    # Extrair informações do produto
    product_info = shopee_service.extract_product_info(product_url)
    print(product_info)