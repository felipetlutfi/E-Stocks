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
        last_price = float(span_last_price.text.strip().replace(',', ''))
        return last_price
    else:
        return None

def get_us10y_price_previous_day():
    url = f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202401"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todas as ocorrências da tag td com os atributos específicos
        td_elements = soup.find_all('td', {'headers': 'view-field-bc-10year-table-column'}, class_='views-field views-field-field-bc-10year')

        if td_elements:
            # Pegar o texto da última ocorrência
            last_td_element = td_elements[-1]
            yesterday_price = float(last_td_element.text.strip().replace(',', ''))
            return yesterday_price
        else:
            return None
    else:
        return None

def get_us10y_data():
    us10y_price_value = get_us10y_price()
    us10y_price_previous_day_value = get_us10y_price_previous_day()
    
    if us10y_price_value is not None and us10y_price_previous_day_value is not None:
        # Calculando a variação percentual
        percentage_change = ((us10y_price_value - us10y_price_previous_day_value) / us10y_price_previous_day_value) * 100

        data = {
            "US10Y_Price": us10y_price_value,
            "US10Y_Price_Previous_Day": us10y_price_previous_day_value,
            "Percentage_Change": round(percentage_change, 2)
        }
        return data
    else:
        return {"error": "Erro ao obter a cotação do Tesouro Americano de 10 anos"}

@app.route('/us10y_data', methods=['GET'])
def us10y_data_route():
    us10y_data = get_us10y_data()
    return jsonify(us10y_data)

if __name__ == "__main__":
    app.run(debug=True)
