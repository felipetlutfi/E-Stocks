import requests
from bs4 import BeautifulSoup
import json

# Defina a URL alvo
url = "https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/"

# Faça a solicitação HTTP e obtenha o conteúdo HTML
response = requests.get(url)
html_content = response.text

# Use o BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html_content, "html.parser")

# Encontre a <div class="tables">
div_tables = soup.find("div", class_="tables")

# Encontre a tabela desejada
tabela_fechamento = div_tables.find("td", string="Fechamento anterior")

# Extraia a informação do "Fechamento anterior"
fechamento_anterior = tabela_fechamento.find_next("td").text.strip()

# Encontre o elemento <div class="value">
div_value = soup.find("div", class_="value")

# Encontre o elemento <p> dentro da <div class="value">
p_element = div_value.find("p")

# Obtenha o texto do elemento <p>
cotacao_atual = p_element.text.strip()

# Converta os valores para float
cotacao_atual = float(cotacao_atual.replace(',', '.'))
fechamento_anterior = float(fechamento_anterior.replace(',', '.'))

# Calcule a diferença percentual
diferenca_percentual = ((cotacao_atual - fechamento_anterior) / fechamento_anterior) * 100

# Crie um dicionário JSON com as informações desejadas
json_data = {
    "cotacao_atual": cotacao_atual,
    "fechamento_anterior": fechamento_anterior,
    "diferenca_percentual": round(diferenca_percentual,2)
}

# Imprima ou faça o que quiser com o JSON
print(json.dumps(json_data, indent=2))
