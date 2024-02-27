import requests
from bs4 import BeautifulSoup

url = 'https://investidor10.com.br/indices/cdi/'

# Fazendo a solicitação HTTP
response = requests.get(url)

# Verificando se a solicitação foi bem-sucedida (código 200)
if response.status_code == 200:
    # Parseando o conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrando a tag b dentro da classe description
    tag_b = soup.find('div', class_='description').find('b')

    # Obtendo o conteúdo da tag b
    conteudo_b = tag_b.text

    print(f"O valor do CDI hoje é: {conteudo_b}")
else:
    print(f"Falha na solicitação. Código de status: {response.status_code}")
