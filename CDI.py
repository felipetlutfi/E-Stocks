from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/cdi', methods=['GET'])
def get_cdi():
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
            return jsonify({"CDI_hoje": cdi_value})
        else:
            return jsonify({"error": "Nenhuma tag <b> encontrada dentro da div."}), 500
    else:
        return jsonify({"error": "Div com a classe 'description' não encontrada."}), 500

if __name__ == '__main__':
    app.run(debug=True)
