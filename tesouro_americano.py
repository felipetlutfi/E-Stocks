from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

def get_us10y_price(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        td_element = soup.find('td', headers='view-field-bc-10year-table-column', class_='views-field views-field-field-bc-10year')
        price = td_element.text.strip()
        return price
    else:
        return None

@app.route('/us10y_prices', methods=['GET'])
def us10y_prices():
    # Obter a cotação de hoje
    url_today = "https://www.cnbc.com/quotes/US10Y"
    us10y_price_today_value = get_us10y_price(url_today)
    
    # Obter a data de ontem
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y%m%d")
    
    # Obter a cotação de ontem
    url_yesterday = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month={formatted_date}"
    us10y_price_yesterday_value = get_us10y_price(url_yesterday)
    
    if us10y_price_today_value is not None and us10y_price_yesterday_value is not None:
        data = {
            "US10Y_Price_Today": us10y_price_today_value,
            "US10Y_Price_Yesterday": us10y_price_yesterday_value
        }
        return jsonify(data)
    else:
        return jsonify({"error": "Erro ao obter as cotações do Tesouro Americano de 10 anos"}), 500

if __name__ == "__main__":
    app.run(debug=True)
