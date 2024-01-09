from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_us10y_price():
    url = "https://www.cnbc.com/quotes/US10Y"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        span_last_price = soup.find('span', class_='QuoteStrip-lastPrice')
        last_price = span_last_price.text.strip()
        return last_price
    else:
        return None

@app.route('/us10y_price', methods=['GET'])
def us10y_price():
    us10y_price_value = get_us10y_price()
    
    if us10y_price_value is not None:
        data = {"US10Y_Price": us10y_price_value}
        return jsonify(data)
    else:
        return jsonify({"error": "Erro ao obter a cotação do Tesouro Americano de 10 anos"}), 500

if __name__ == "__main__":
    app.run(debug=True)
