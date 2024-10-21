import requests
import json

url = "https://api.foursquare.com/v3/places/4d29b8ef3c795481133ada9b/tips"

headers = {
    "accept": "application/json",
    "Authorization": "fsq37MCRZy+U/HSQ60fH8ngI6FFJBMMa5Oq8Z3X8R/ujxxg="
}

params = {
    "limit": 50,
    "lang": "pt"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()  # Converter resposta para JSON
    # Salvar no arquivo JSON
    with open('foursquare_tips.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Dados salvos em 'foursquare_tips.json'")
else:
    print(f"Erro: {response.status_code}")
