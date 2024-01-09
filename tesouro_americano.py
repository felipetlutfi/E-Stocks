import requests
from bs4 import BeautifulSoup
import json

def get_us10y_price():
    url = "https://www.cnbc.com/quotes/US10Y"
    
    # Faz a requisição HTTP
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Faz o parsing do HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra a tag span com a classe QuoteStrip-lastPrice
        span_last_price = soup.find('span', class_='QuoteStrip-lastPrice')
        
        # Obtém o texto dentro da tag span
        last_price = span_last_price.text.strip()
        
        # Retorna o preço
        return last_price
    else:
        # Se a requisição não foi bem-sucedida, mostra uma mensagem de erro
        print(f"Erro ao obter a página. Código de status: {response.status_code}")
        return None

def main():
    # Obtém o preço do Tesouro Americano de 10 anos
    us10y_price = get_us10y_price()
    
    # Cria um dicionário com o preço
    data = {"US10Y_Price": us10y_price}
    
    # Converte o dicionário para JSON e imprime
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    print(json_data)

if __name__ == "__main__":
    main()
