import requests
import json
import base64

example_genres = ['blues', 'rock', 'soul']

# carregue as chaves
client_id = '6b63eb054e2d4e57b37c62c1a1373c0c'
client_secret = 'f89ebd91fa974d068a260d6cf4dc5802'

def get_token(client_id, client_secret):
    base64_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'headers': {
            'Authorization': 'Basic ' + base64_auth, 
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        'data': {
            'grant_type': 'client_credentials'
        }
    }

    response = requests.post(auth_options['url'], headers=auth_options['headers'], data=auth_options['data'])

    if response.status_code == 200:
        r = response.json()
        token = r['access_token']
        token_type = r['token_type']
        token_duration = r['expires_in']
        print(f'Token de Acesso requisitado com sucesso!')
        print(f'Tipo do Token: {token_type}')
        print(f'Disponibilidade do Token: {token_duration} segundos')
        return f'{token_type} {token}'
    else:
        print('Não foi possível obter o token de acesso')
        return None

# teste da função
access_token = get_token(client_id, client_secret)

def api_call(url, access_token):
    if access_token:
        response = requests.get(url, headers={'Authorization': access_token})
        if response.status_code == 200:
            api_response = response.json()
            
            # Grava o JSON em um arquivo
            with open('spotify_data.json', 'w') as f:
                json.dump(api_response, f, indent=2)
            
            print("Resposta salva em spotify_data.json")
            return api_response
        else:
            print(f"Erro na requisição: {response.status_code}")
            return None
    else:
        print("Token de acesso não disponível.")
        return None

# definindo nosso endpoint com base na documentação
url = 'https://api.spotify.com/v1/search?q=genre:rock&type=track&market=BR&limit=20&offset=0'

# se a requisição estiver correta, ela deve salvar o JSON no arquivo
api_call(url, access_token)
