from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_second_element(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&apikey=042540f5cf714a688d32ac593f8acf8f&source=docs"
    response = requests.get(url)
    data = response.json()

    # Verifica se existem pelo menos dois elementos e retorna o segundo elemento
    if 'values' in data and len(data['values']) >= 2:
        return data['values'][1]
    else:
        return None

def calculate_percentage_difference(open_price, close_price):
    if open_price != 0:
        return ((float(close_price) - float(open_price)) / float(open_price)) * 100
    else:
        return None

@app.route('/cotacoes_internacionais', methods=['GET'])
def get_quotes():
    assets = {
        'S&P 500': 'GSPC',
        'Nasdaq': 'IXIC',
        'BTCUSD': 'BTC/USD',
        'USDBRL': 'USD/BRL'
    }

    results = {}

    for asset, symbol in assets.items():
        second_element = get_second_element(symbol)
        if second_element:
            open_price = second_element.get('open', 0)
            close_price = second_element.get('close', 0)

            difference_percentual = calculate_percentage_difference(open_price, close_price)
            results[asset] = {
                'close': close_price,
                'diferenca_percentual': difference_percentual
            }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
