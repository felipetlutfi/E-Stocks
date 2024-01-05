from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/maiores_baixas', methods=['GET'])
def obter_dados():
    url = "https://statusinvest.com.br/acoes/variacao/ibovespa"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        input_element = soup.find('input', {'id': 'result', 'name': 'result', 'type': 'hidden'})

        if input_element:
            result_value = input_element.get('value')
            dados = json.loads(result_value)

            # Ordena os dados com base no valor de 'resultPercentageValue'
            dados_ordenados = sorted(dados, key=lambda x: float(x['resultPercentageValue']))

            # Seleciona os três elementos com os menores valores
            indices_desejados = dados_ordenados[]

            # Retorna os dados selecionados como JSON
            return jsonify(indices_desejados)

        else:
            return jsonify({"error": "Elemento não encontrado."})

    else:
        return jsonify({"error": f"Erro ao acessar a URL. Código de status: {response.status_code}"})

if __name__ == '__main__':
    app.run(debug=True)
