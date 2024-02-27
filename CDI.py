import requests
from bs4 import BeautifulSoup
import json

# URL da página com o índice CDI
url = "https://investidor10.com.br/indices/cdi/"

# Faz a requisição HTTP para obter o conteúdo da página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Encontra a div com a classe "description"
div_description = soup.find("div", class_="description")

# Verifica se a div foi encontrada antes de tentar extrair o texto
if div_description:
    # Encontra todas as tags <b> dentro da div
    b_tags = div_description.find_all("b")

    # Extrai o valor dentro da primeira tag <b>
    if b_tags:
        cdi_value = b_tags[0].get_text()
        
        # Cria um dicionário com o valor do CDI hoje
        cdi_json = {"CDI_hoje": cdi_value}

        # Converte o dicionário para JSON
        cdi_json_str = json.dumps(cdi_json, ensure_ascii=False, indent=2)

        print(cdi_json_str)
    else:
        print("Nenhuma tag <b> encontrada dentro da div.")
else:
    print("Div com a classe 'description' não encontrada.")
