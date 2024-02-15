from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/api/ipca', methods=['GET'])
def get_ipca_info():
    # URL da página alvo
    url = 'https://investidor10.com.br/indices/ipca/#:~:text=Qual%20o%20IPCA%20hoje%3F,de%202023%20foi%20de%204.62%25.'

    # Fazendo a requisição HTTP
    response = requests.get(url)

    # Verificando se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Obtendo o conteúdo HTML da página
        html_content = response.content

        # Criando um objeto BeautifulSoup para análise HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrando a tag desejada
        tag_td = soup.find('td', {'style': 'background-color: #dedede', 'class': 'text-center'})

        # Extraindo o texto da tag
        info_text = tag_td.text.strip()

        # Criando um dicionário para o JSON
        result_dict = {'info': info_text}

        return jsonify(result_dict)

    else:
        return jsonify({'error': f'Falha na requisição. Código de status: {response.status_code}'})

if __name__ == '__main__':
    app.run(debug=True)
