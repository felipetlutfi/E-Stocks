from flask import Flask, jsonify
import requests

app = Flask(__name__)

def obter_cotacao_tesouro_10_anos(api_key):
    # URL da API Alpha Vantage para obter informações sobre o Tesouro Americano de 10 anos
    api_url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&maturity=10y&interval=daily&apikey={api_key}"

    # Fazendo a solicitação à API
    response = requests.get(api_url)
    data = response.json()

    if 'data' in data and data['data']:
        primeiro_elemento = data['data'][0]

        primeiro_date = primeiro_elemento.get('date', None)
        primeiro_value = primeiro_elemento.get('value', None)

        return {
            "primeiro_date": primeiro_date,
            "primeiro_value": primeiro_value,
        }
    else:
        return {"error": "Não foi possível obter dados suficientes da API."}

@app.route('/cotacao_tesouro_10_anos')
def cotacao_tesouro_10_anos():
    # Insira sua chave de API da Alpha Vantage aqui
    api_key = "C12M6F5RNUP4MWL9"

    # Obtendo o resultado da função
    resultado = obter_cotacao_tesouro_10_anos(api_key)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
