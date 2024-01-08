from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

def obter_cotacao_tesouro_10_anos(api_key):
    # URL da API Alpha Vantage para obter informações sobre o Tesouro Americano de 10 anos
    api_url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&maturity=10y&interval=daily&apikey={api_key}"

    # Fazendo a solicitação à API
    response = requests.get(api_url)

    if response.status_code == 200:
        # Convertendo a resposta para JSON
        data = response.json()

        # Obtendo informações relevantes
        if 'data' in data and len(data['data']) >= 2:
            primeiro_elemento = data['data'][0]
            segundo_elemento = data['data'][1]

            primeiro_date = primeiro_elemento.get('date', None)
            primeiro_value = primeiro_elemento.get('value', None)

            segundo_date = segundo_elemento.get('date', None)
            segundo_value = segundo_elemento.get('value', None)

            # Calculando a variação percentual
            if primeiro_value is not None and segundo_value is not None:
                variacao_percentual = ((float(primeiro_value) - float(segundo_value)) / abs(float(segundo_value))) * 100
            else:
                variacao_percentual = None

            # Criando um dicionário com os resultados desejados
            resultado = {
                "primeiro_date": primeiro_date,
                "primeiro_value": primeiro_value,
                "segundo_date": segundo_date,
                "segundo_value": segundo_value,
                "variacao_percentual": variacao_percentual
            }

            # Convertendo o dicionário para formato JSON
            resultado_json = json.dumps(resultado, indent=2)
            return resultado_json
        else:
            return "Não foram encontrados dados suficientes."

    else:
        return f"Erro ao obter dados. Código de status: {response.status_code}"

# Rota para obter a cotação do Tesouro Americano de 10 anos
@app.route('/cotacao_tesouro_10_anos')
def cotacao_tesouro_10_anos():
    # Insira sua chave de API da Alpha Vantage aqui
    api_key = "C12M6F5RNUP4MWL9"

    # Chame a função para obter a cotação
    resultado_json = obter_cotacao_tesouro_10_anos(api_key)

    # Retorne o resultado como uma resposta JSON
    return jsonify(resultado_json)

if __name__ == '__main__':
    app.run(debug=True)
