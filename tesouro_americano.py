from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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

def get_us10y_price_previous_day():
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y%m%d")

    url = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month={date_str}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        td_element = soup.find('td', {'headers': 'view-field-bc-10year-table-column'})
        if td_element:
            return td_element.text.strip()
    return None

@app.route('/us10y_data', methods=['GET'])
def us10y_data():
    us10y_price_value = get_us10y_price()
    us10y_price_previous_day_value = get_us10y_price_previous_day()
    
    if us10y_price_value is not None and us10y_price_previous_day_value is not None:
        data = {
            "US10Y_Price": us10y_price_value,
            "US10Y_Price_Previous_Day": us10y_price_previous_day_value
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Erro ao obter a cotação do Tesouro Americano de 10 anos"}), 500

if __name__ == "__main__":
    app.run(debug=True)
