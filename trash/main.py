import os
import random
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.externals.shopee.use_case.extract_product_info import extract_product_info

print("Iniciando o navegador...")
# Usar undetected-chromedriver para evitar detecção
options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-web-security')
options.add_argument('--disable-features=IsolateOrigins,site-per-process')
options.add_argument('--disable-site-isolation-trials')

# Adicionar user-agent mais convincente
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.2623.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
]
options.add_argument(f'user-agent={random.choice(user_agents)}')

# Inicializar o driver com undetected-chromedriver e versão específica
driver = uc.Chrome(
    options=options,
    version_main=134,  # Especificar a versão do Chrome
    use_subprocess=True  # Usar subprocesso para melhor compatibilidade
)

# Definir o tamanho da janela para simular um navegador real
driver.set_window_size(1366, 768)

# Executar JavaScript para ocultar que estamos usando Selenium
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US', 'en']})")

# Dados de login
email = "pedro.emserh@gmail.com"
senha = "Senha051199"

# Acessar a página inicial da Shopee
print("Acessando a página inicial da Shopee...")
driver.get("https://shopee.com.br/")
time.sleep(random.uniform(3, 5))  # Tempo aleatório para parecer mais humano

# Fechar o pop-up de localização se aparecer
try:
    popup_close_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".shopee-popup__close-btn"))
    )
    popup_close_button.click()
    print("Pop-up fechado com sucesso")
    time.sleep(random.uniform(1, 2))
except Exception as e:
    print(f"Nenhum pop-up encontrado ou erro ao fechar: {e}")

# Clicar no botão de login
try:
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar__link--account, [data-sqe='login']"))
    )
    login_button.click()
    print("Botão de login clicado com sucesso")
    time.sleep(random.uniform(2, 3))
except Exception as e:
    print(f"Erro ao clicar no botão de login: {e}")
    try:
        # Tentar alternativa se o primeiro seletor falhar
        login_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Login')]")
        login_button.click()
        print("Botão de login alternativo clicado com sucesso")
        time.sleep(random.uniform(2, 3))
    except Exception as e:
        print(f"Erro ao clicar no botão de login alternativo: {e}")

# Preencher email
try:
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][name='loginKey'], input[type='email']"))
    )
    # Limpar o campo antes de digitar
    email_field.clear()
    # Digitar lentamente para simular comportamento humano
    for char in email:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    print("Email digitado com sucesso")
    time.sleep(random.uniform(1, 2))
except Exception as e:
    print(f"Erro ao preencher o campo de email: {e}")

# Preencher senha
try:
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
    )
    password_field.clear()
    # Digitar lentamente para simular comportamento humano
    for char in senha:
        password_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    print("Senha digitada com sucesso")
    time.sleep(random.uniform(1, 2))
except Exception as e:
    print(f"Erro ao preencher o campo de senha: {e}")

# Clicar no botão para fazer login
try:
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], .btn-solid-primary"))
    )
    submit_button.click()
    print("Botão de enviar login clicado com sucesso")
    
    # Verificar se há captcha e pausar para intervenção manual
    print("\n" + "="*50)
    print("ATENÇÃO: Se um captcha aparecer, resolva-o manualmente agora.")
    print("O programa está pausado para permitir que você resolva o captcha.")
    print("Após resolver o captcha, digite 'continuar' e pressione Enter.")
    print("="*50 + "\n")
    
    user_input = input("Digite 'continuar' para prosseguir após resolver o captcha: ")
    while user_input.lower() != 'continuar':
        user_input = input("Por favor, digite 'continuar' para prosseguir: ")
    
    print("Continuando a execução do script...")
    # Dar tempo para o login ser processado
    time.sleep(random.uniform(5, 10))
except Exception as e:
    print(f"Erro ao clicar no botão de enviar login: {e}")

# Verificar se o login foi bem-sucedido
try:
    # Tentar encontrar elementos que indicam que estamos logados
    logged_in_indicators = [
        "span.navbar__username",
        ".shopee-avatar",
        ".stardust-avatar",
        ".shopee-avatar__img"
    ]
    
    logged_in = False
    for selector in logged_in_indicators:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element:
                logged_in = True
                print(f"Elemento de usuário logado encontrado: {selector}")
                break
        except:
            continue
    
    if logged_in:
        print("Usuário parece estar logado com sucesso!")
    else:
        print("Não foi possível confirmar se o usuário está logado. Continuando mesmo assim...")
except Exception as e:
    print(f"Erro ao verificar status de login: {e}")

# Agora que estamos logados, tentar acessar a página de flash sale
time.sleep(5)
url = "https://shopee.com.br/flash_sale"
print(f"Acessando URL: {url}")
driver.get(url)
print("Aguardando carregamento da página...")
time.sleep(random.uniform(10, 15))  # Tempo aleatório para parecer mais humano

# Simular comportamento humano com movimentos aleatórios
for i in range(3):
    scroll_amount = random.randint(200, 800)
    driver.execute_script(f"window.scrollTo(0, {scroll_amount})")
    time.sleep(random.uniform(0.5, 1.5))

# Salvar screenshot para debug
print("Salvando screenshot...")
driver.save_screenshot("shopee_page.png")
print(f"Screenshot salvo em: {os.path.abspath('shopee_page.png')}")

# Salvar o HTML da página para debug
print("Salvando HTML da página...")
with open("shopee_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print(f"HTML salvo em: {os.path.abspath('shopee_page.html')}")

# Imprimir a URL atual para debug
print(f"URL atual: {driver.current_url}")

# Coleta os produtos
print("Buscando produtos...")
produtos = driver.find_elements(By.CSS_SELECTOR, "div.V6A28M div.sGJRNY")
print(f"Encontrados {len(produtos)} produtos")

# Tentar outros seletores se o original não funcionar
if len(produtos) == 0:
    print("Tentando seletores alternativos...")
    # Tentar encontrar qualquer produto na página
    produtos = driver.find_elements(By.CSS_SELECTOR, ".shopee-search-item-result__item")
    print(f"Seletor alternativo 1: Encontrados {len(produtos)} produtos")
    
    if len(produtos) == 0:
        produtos = driver.find_elements(By.CSS_SELECTOR, ".flash-sale-item-card")
        print(f"Seletor alternativo 2: Encontrados {len(produtos)} produtos")
        
        if len(produtos) == 0:
            produtos = driver.find_elements(By.CSS_SELECTOR, "div[data-sqe='item']")
            print(f"Seletor alternativo 3: Encontrados {len(produtos)} produtos")
            
            if len(produtos) == 0:
                produtos = driver.find_elements(By.CSS_SELECTOR, ".flash-sale-item-card-link")
                print(f"Seletor alternativo 4: Encontrados {len(produtos)} produtos")
                
                if len(produtos) == 0:
                    produtos = driver.find_elements(By.CSS_SELECTOR, ".flash-sale-item-card-wrapper")
                    print(f"Seletor alternativo 5: Encontrados {len(produtos)} produtos")
                    
                    if len(produtos) == 0:
                        # Tentar seletores mais genéricos
                        produtos = driver.find_elements(By.CSS_SELECTOR, ".shopee-item-card")
                        print(f"Seletor alternativo 6: Encontrados {len(produtos)} produtos")
                        
                        if len(produtos) == 0:
                            produtos = driver.find_elements(By.CSS_SELECTOR, "a[data-sqe='link']")
                            print(f"Seletor alternativo 7: Encontrados {len(produtos)} produtos")

dados_produtos = []
for i, produto in enumerate(produtos):
    try:
        print(f"Extraindo produto {i+1}/{len(produtos)}...")
        
        # Tentar diferentes seletores para o nome do produto
        try:
            nome = produto.find_element(By.CSS_SELECTOR, "div.UeJ6lG").text
        except:
            try:
                nome = produto.find_element(By.CSS_SELECTOR, ".ie3A+n").text
            except:
                try:
                    nome = produto.find_element(By.CSS_SELECTOR, "div[data-sqe='name']").text
                except:
                    try:
                        nome = produto.find_element(By.CSS_SELECTOR, ".flash-sale-item-card-title").text
                    except:
                        try:
                            nome = produto.find_element(By.CSS_SELECTOR, ".shopee-item-card__text-name").text
                        except:
                            nome = "Nome não encontrado"
        
        # Tentar obter o preço com desconto (preço atual)
        try:
            preco_atual = produto.find_element(By.CSS_SELECTOR, "div.I99cV_ div.Gt3dn4 strong.Rgk_yn").text
        except:
            try:
                preco_atual = produto.find_element(By.CSS_SELECTOR, ".ZEgDH9").text
            except:
                try:
                    preco_atual = produto.find_element(By.CSS_SELECTOR, "span.shopee-item-card__current-price").text
                except:
                    try:
                        preco_atual = produto.find_element(By.CSS_SELECTOR, ".flash-sale-item-card-current-price").text
                    except:
                        try:
                            preco_atual = produto.find_element(By.CSS_SELECTOR, ".shopee-price-lowered__current").text
                        except:
                            preco_atual = "Preço atual não encontrado"
        
        # Tentar obter o preço original
        try:
            preco_original = produto.find_element(By.CSS_SELECTOR, "div.I99cV_.zbggAt strong.Rgk_yn").text
        except:
            try:
                preco_original = produto.find_element(By.CSS_SELECTOR, ".shopee-price-lowered__original").text
            except:
                try:
                    preco_original = produto.find_element(By.CSS_SELECTOR, ".flash-sale-item-card-original-price").text
                except:
                    try:
                        preco_original = produto.find_element(By.CSS_SELECTOR, ".shopee-item-card__original-price").text
                    except:
                        preco_original = preco_atual  # Se não encontrar, usa o preço atual
        
        # Tentar obter o desconto
        try:
            desconto = produto.find_element(By.CSS_SELECTOR, "div.hcYtZZ").text
        except:
            try:
                desconto = produto.find_element(By.CSS_SELECTOR, ".shopee-price-lowered__percentage").text
            except:
                try:
                    desconto = produto.find_element(By.CSS_SELECTOR, ".flash-sale-item-card-discount").text
                except:
                    try:
                        desconto = produto.find_element(By.CSS_SELECTOR, ".shopee-item-card__discount").text
                    except:
                        desconto = "Sem desconto"
        
        # Tentar obter o link
        try:
            link = produto.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            try:
                # Se o próprio elemento for um link
                link = produto.get_attribute("href")
            except:
                link = "Link não encontrado"
        
        # Tentar obter a imagem
        try:
            # Tentar o novo seletor fornecido pelo usuário
            imagem_div = produto.find_element(By.CSS_SELECTOR, "div.xe3g4p.H7sp0t")
            imagem_style = imagem_div.get_attribute("style")
            
            # Extrair a URL da string de estilo
            if "background-image: url(" in imagem_style:
                inicio = imagem_style.find('url("') + 5
                fim = imagem_style.find('")', inicio)
                if inicio != -1 and fim != -1:
                    imagem = imagem_style[inicio:fim]
                else:
                    # Tenta outro formato de URL
                    inicio = imagem_style.find("url('") + 5
                    fim = imagem_style.find("')", inicio)
                    if inicio != -1 and fim != -1:
                        imagem = imagem_style[inicio:fim]
        except:
            try:
                # Alternativa usando o seletor anterior
                imagem_div = produto.find_element(By.CSS_SELECTOR, "div.aXY7Pt")
                imagem_style = imagem_div.get_attribute("style")
                
                # Extrair a URL da string de estilo
                if "background-image" in imagem_style:
                    inicio = imagem_style.find('url("') + 5
                    fim = imagem_style.find('")', inicio)
                    if inicio != -1 and fim != -1:
                        imagem = imagem_style[inicio:fim]
                    else:
                        # Tenta outro formato de URL
                        inicio = imagem_style.find("url('") + 5
                        fim = imagem_style.find("')", inicio)
                        if inicio != -1 and fim != -1:
                            imagem = imagem_style[inicio:fim]
                else:
                    try:
                        # Tenta encontrar qualquer elemento img
                        imagem_elem = produto.find_element(By.CSS_SELECTOR, "img")
                        imagem = imagem_elem.get_attribute("src")
                    except:
                        try:
                            # Tenta encontrar qualquer div com background-image
                            elements = produto.find_elements(By.CSS_SELECTOR, "div[style*='background-image']")
                            if elements:
                                imagem_style = elements[0].get_attribute("style")
                                
                                # Extrair a URL entre url(" e ")
                                inicio = imagem_style.find('url("') + 5
                                fim = imagem_style.find('")', inicio)
                                if inicio != -1 and fim != -1:
                                    imagem = imagem_style[inicio:fim]
                                else:
                                    # Tenta outro formato de URL
                                    inicio = imagem_style.find("url('") + 5
                                    fim = imagem_style.find("')", inicio)
                                    if inicio != -1 and fim != -1:
                                        imagem = imagem_style[inicio:fim]
                                    else:
                                        imagem = "Imagem não encontrada"
                            else:
                                imagem = "Imagem não encontrada"
                        except:
                            imagem = "Imagem não encontrada"
            except:
                imagem = "Imagem não encontrada"
        
        dados_produtos.append({
            "nome": nome,
            "preco_atual": preco_atual,
            "preco_original": preco_original,
            "desconto": desconto,
            "link": link,
            "imagem": imagem
        })
        print(f"Produto {i+1} extraído com sucesso: {nome}")
        time.sleep(random.uniform(0.1, 0.3))  # Pequeno delay entre cada produto
    except Exception as e:
        print(f"Erro ao extrair produto {i+1}: {e}")

# Fecha o navegador
print("Fechando o navegador...")
driver.quit()

# Exibe os produtos extraídos
print("\nProdutos extraídos:")
if dados_produtos:
    for i, produto in enumerate(dados_produtos):
        print(f"{i+1}. {produto['nome']} - Preço atual: {produto['preco_atual']} - Preço original: {produto['preco_original']} - Desconto: {produto['desconto']}")
else:
    print("Nenhum produto foi extraído.")

print(f"\nTotal de produtos extraídos: {len(dados_produtos)}")

# Salvar os produtos em um arquivo JSON
if dados_produtos:
    import json
    with open("produtos_shopee.json", "w", encoding="utf-8") as f:
        json.dump(dados_produtos, f, ensure_ascii=False, indent=4)
    print(f"Produtos salvos em: {os.path.abspath('produtos_shopee.json')}")

product_url = "https://shopee.com.br/product/123456/789012"
product_info = extract_product_info(product_url)

if product_info:
    print(f"Image URL: {product_info.image_url}")
    print(f"Affiliate Link: {product_info.affiliate_link}")
    print(f"Sales Text: {product_info.sales_text}")
