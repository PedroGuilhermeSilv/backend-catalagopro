# Extração de Dados da Shopee

Este repositório contém diferentes abordagens para extrair dados de produtos da Shopee. Devido às proteções anti-scraping implementadas pela Shopee, oferecemos várias alternativas para obter os dados desejados.

## Arquivos Disponíveis

1. **main.py** - Script original usando Selenium para tentar fazer scraping direto do site (enfrenta problemas com proteções anti-bot)
2. **shopee_api_client.py** - Cliente para a API não oficial da Shopee (abordagem recomendada)
3. **shopee_api_example.py** - Exemplo conceitual usando serviços de proxy para contornar proteções
4. **shopee_scraper_alternatives.py** - Documento explicativo sobre as limitações e alternativas para scraping da Shopee

## Desafios do Web Scraping na Shopee

A Shopee implementa várias proteções contra scraping:

- Redirecionamento forçado para a página de login
- Detecção de automação (Selenium)
- Verificação de fingerprinting do navegador
- Bloqueio de IP após múltiplas requisições
- Uso de IDs de rastreamento (como `fu_tracking_id`)
- Possível uso de reCAPTCHA ou tecnologias similares

## Abordagens Recomendadas

### 1. Usando a API Não Oficial (Recomendado)

O script `shopee_api_client.py` utiliza as mesmas APIs que o aplicativo móvel da Shopee usa, oferecendo uma maneira mais confiável de obter dados.

Para usar:
```bash
python shopee_api_client.py
```

Este script oferece várias funcionalidades:
- Obter produtos em promoção relâmpago
- Pesquisar produtos por palavra-chave
- Obter produtos de uma categoria específica
- Obter detalhes completos de um produto
- Obter pesquisas em tendência

### 2. Usando Serviços de Proxy

O script `shopee_api_example.py` demonstra como usar serviços de proxy especializados (como ScraperAPI, BrightData, etc.) para contornar as proteções da Shopee.

**Nota:** Este é um exemplo conceitual e requer uma chave de API de um serviço de proxy para funcionar.

### 3. Usando Selenium (Desafios)

O script original `main.py` tenta usar Selenium para fazer scraping direto do site da Shopee, mas enfrenta vários desafios com as proteções anti-bot. Esta abordagem não é recomendada devido à sua baixa taxa de sucesso.

## Considerações Legais

Antes de usar qualquer uma dessas abordagens, considere:

1. Verifique os Termos de Serviço da Shopee para garantir que você não está violando suas políticas
2. Use os dados apenas para fins pessoais ou de pesquisa
3. Respeite limites de taxa para não sobrecarregar os servidores
4. Considere usar APIs oficiais se disponíveis para seu caso de uso

## Requisitos

```
requests
beautifulsoup4
selenium
webdriver-manager
```

Instale as dependências com:
```bash
pip install -r requirements.txt
```

## Arquivo de Requisitos

Também incluímos um arquivo `requirements.txt` para facilitar a instalação das dependências necessárias.

## Contribuições

Contribuições são bem-vindas! Se você encontrou uma maneira melhor de extrair dados da Shopee ou tem sugestões para melhorar os scripts existentes, sinta-se à vontade para abrir um pull request. 