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

# Extrai o texto dentro da div
cdi_text = div_description.get_text()

# Filtra o valor do CDI hoje
cdi_today = None
for line in cdi_text.split("\n"):
    if "CDI hoje" in line:
        cdi_today = line.split(":")[1].strip()

# Cria um dicionário com o valor do CDI hoje
cdi_json = {"CDI_hoje": cdi_today}

# Converte o dicionário para JSON
cdi_json_str = json.dumps(cdi_json, ensure_ascii=False, indent=2)

print(cdi_json_str)
