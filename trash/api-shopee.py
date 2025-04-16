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

# Exemplo de uso
if __name__ == "__main__":
    # URL de exemplo
    url = "https://shopee.com.br/Ferro-de-Passar-Roupa-a-Vapor-Cer%C3%A2mica-GCSTBS5956-Preto-e-Roxo-Oster-i.1314243679.22893220448"
    
    # Gerar o short link
    result = generate_short_link(url)
    print("Resultado:", json.dumps(result, indent=2))