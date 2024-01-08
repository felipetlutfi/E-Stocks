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
        time_series_data = data.get('Time Series (Daily)', {})
        if not time_series_data:
            return "Não foram encontrados dados suficientes."

        dates = list(time_series_data.keys())[:2]
        if len(dates) > 2:
            return "Não foram encontrados dados suficientes."

        primeiro_elemento = time_series_data[dates[0]]
        segundo_elemento = time_series_data[dates[1]]

        primeiro_date = dates[0]
        primeiro_value = primeiro_elemento.get('1. open', None)

        segundo_date = dates[1]
        segundo_value = segundo_elemento.get('1. open', None)

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
