from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_cdi_value():
    url = "https://investidor10.com.br/indices/cdi/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar a div com a classe "description"
    div_description = soup.find("div", class_="description")

    if div_description:
        # Encontrar todas as tags <b> dentro da div
        b_tags = div_description.find_all("b")
        # Obter o texto da segunda tag <b>
        cdi_value = b_tags[1].get_text()
        return cdi_value



@app.route('/cdi', methods=['GET'])
def get_cdi():
    cdi_value = get_cdi_value()

    if cdi_value:
        return jsonify({"CDI_hoje": cdi_value})
    else:
        return jsonify({"error": "Valor do CDI não encontrado"}), 500

if __name__ == '__main__':
    app.run(debug=True)
