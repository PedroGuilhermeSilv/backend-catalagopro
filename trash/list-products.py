import hashlib
import json
import time

import requests

# Credenciais
app_id = "18365700060"
secret = "K6R6PQPQCFQU2CST6B4QGJ6P6FPN4PYG"

def generate_short_link(url):
    # Timestamp atual em segundos
    timestamp = int(time.time())
    
    # Query para gerar o short link
    query = f'''mutation{{
        generateShortLink(input:{{
            originUrl:"{url}",
            subIds:["s1","s2","s3","s4","s5"]
        }}){{
            shortLink
        }}
    }}'''
    
    # Criar o payload
    payload = json.dumps({"query": query})
    
    # Construir o fator de assinatura
    factor = f"{app_id}{timestamp}{payload}{secret}"
    
    # Calcular a assinatura SHA256
    signature = hashlib.sha256(factor.encode()).hexdigest()
    
    # Montar o cabeçalho Authorization
    auth_header = f"SHA256 Credential={app_id}, Timestamp={timestamp}, Signature={signature}"
    
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

def list_products(keyword=None, sort_type=1, page=1, limit=1, shop_id=None, item_id=None, product_cat_id=None):
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
    factor = f"{app_id}{timestamp}{payload}{secret}"
    
    # Calcular a assinatura SHA256
    signature = hashlib.sha256(factor.encode()).hexdigest()
    
    # Montar o cabeçalho Authorization
    auth_header = f"SHA256 Credential={app_id}, Timestamp={timestamp}, Signature={signature}"
    
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

def list_shop_offers(shop_id=None, keyword=None, shop_type=None, is_key_seller=None, sort_type=1, seller_comm_cove_ratio=None, page=1, limit=10):
    # Timestamp atual em segundos
    timestamp = int(time.time())
    
    # Construir os argumentos da query
    args = []
    if shop_id:
        args.append(f'shopId:{shop_id}')
    if keyword:
        args.append(f'keyword:"{keyword}"')
    if shop_type:
        args.append(f'shopType:{shop_type}')
    if is_key_seller is not None:
        args.append(f'isKeySeller:{str(is_key_seller).lower()}')
    if sort_type:
        args.append(f'sortType:{sort_type}')
    if seller_comm_cove_ratio:
        args.append(f'sellerCommCoveRatio:"{seller_comm_cove_ratio}"')
    if page:
        args.append(f'page:{page}')
    if limit:
        args.append(f'limit:{limit}')
    
    # Query para listar ofertas de lojas
    query = f'''query{{
        shopOfferV2({','.join(args)}){{
            nodes{{
                commissionRate
                imageUrl
                offerLink
                originalLink
                shopId
                shopName
                ratingStar
                shopType
                remainingBudget
                periodStartTime
                periodEndTime
                sellerCommCoveRatio
                bannerInfo{{
                    count
                    banners{{
                        fileName
                        imageUrl
                        imageSize
                        imageWidth
                        imageHeight
                    }}
                }}
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
    factor = f"{app_id}{timestamp}{payload}{secret}"
    
    # Calcular a assinatura SHA256
    signature = hashlib.sha256(factor.encode()).hexdigest()
    
    # Montar o cabeçalho Authorization
    auth_header = f"SHA256 Credential={app_id}, Timestamp={timestamp}, Signature={signature}"
    
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

# Exemplo de uso
if __name__ == "__main__":
    # Query the product using itemId and shopId
    products = list_products()
    print("\nResultado listagem de produtos:", json.dumps(products, indent=2))

    # Query the shop offers using shopId
    # shop_offers = list_shop_offers(shop_id=84499012, sort_type=2, page=1, limit=10)
    # print("\nResultado listagem de ofertas de lojas:", json.dumps(shop_offers, indent=2))