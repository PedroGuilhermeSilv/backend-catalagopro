import hashlib
import json
import time
from dataclasses import dataclass
from typing import Optional

import requests

from src.core.externals.shopee.connection import Connection


@dataclass
class ProductOutput:
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


@dataclass
class ListProductsOutput:
    data: ProductOutput

@dataclass
class UCListProducts:
    connection: Connection

    def execute(self) -> ListProductsOutput:
        # Get the raw response from the API
        response = self.request_products()
        
        # Extract the product data from the response
        product_data = response['data']['productOfferV2']
        
        # Transform nodes into ProductOutput objects
        nodes = [
            ProductOutput(
                item_id=node['itemId'],
                product_name=node['productName'],
                price_min=node['priceMin'],
                price_max=node['priceMax'],
                commission_rate=node['commissionRate'],
                sales=node['sales'],
                rating_star=node['ratingStar'],
                image_url=node['imageUrl'],
                product_link=node['productLink'],
                offer_link=node['offerLink'],
                shop_name=node['shopName'],
                shop_id=node['shopId']
            )
            for node in product_data['nodes']
        ]
        
        # Return the first product in the list
        return ListProductsOutput(data=nodes)

    def request_products(
        self,
        keyword: Optional[str] = None,
        sort_type: int = 1,
        page: int = 1,
        limit: int = 50,
        shop_id: Optional[int] = None,
        item_id: Optional[int] = None,
        product_cat_id: Optional[int] = None
    ) -> dict:
        # Timestamp atual em segundos
        timestamp = int(time.time())
        
        # Construir os argumentos da query
        args = []
        if keyword:
            args.append(f'keyword:"{keyword}"')
        if sort_type:
            args.append(f'sortType:{sort_type}')
        if page:
            args.append(f'page:{page}')
        if limit:
            args.append(f'limit:{limit}')
        if shop_id:
            args.append(f'shopId:{shop_id}')
        if item_id:
            args.append(f'itemId:{item_id}')
        if product_cat_id:
            args.append(f'productCatId:{product_cat_id}')
        
        # Query para listar produtos
        query = f'''query{{
            productOfferV2({','.join(args)}){{
                nodes{{
                    itemId
                    productName
                    priceMin
                    priceMax
                    commissionRate
                    sales
                    ratingStar
                    imageUrl
                    productLink
                    offerLink
                    shopName
                    shopId
                }}
                pageInfo{{
                    page
                    limit
                    hasNextPage
                }}
            }}
        }}'''
        
        # Criar o payload
        payload = json.dumps({"query": query})
        
        # Construir o fator de assinatura
        factor = f"{self.connection.app_id}{timestamp}{payload}{self.connection.secret}"
        
        # Calcular a assinatura SHA256
        signature = hashlib.sha256(factor.encode()).hexdigest()
        
        # Montar o cabeçalho Authorization
        auth_header = f"SHA256 Credential={self.connection.app_id}, Timestamp={timestamp}, Signature={signature}"
        
        # Headers da requisição
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        
        # URL da API
        url = 'https://open-api.affiliate.shopee.com.br/graphql'
        
        # Fazer a requisição
        response = requests.post(url, headers=headers, data=payload)

        
        # Retornar a resposta
        return response.json()