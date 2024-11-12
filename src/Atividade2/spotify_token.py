import requests
import json
import base64

# Lista de gêneros para buscar
example_genres = ['rock', 'piano', 'jazz', 'pop', 'hip-hop']

# Carregar as chaves
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

# Obter token de acesso
access_token = get_token(client_id, client_secret)

def api_call(url, access_token):
    if access_token:
        response = requests.get(url, headers={'Authorization': access_token})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro na requisição: {response.status_code}")
            return None
    else:
        print("Token de acesso não disponível.")
        return None

# Buscar dados para cada gênero e salvar em um arquivo JSON
all_genre_data = {}
for genre in example_genres:
    url = f'https://api.spotify.com/v1/search?q=genre:{genre}&type=track&market=BR&limit=20&offset=0'
    print(f"Buscando dados para o gênero: {genre}")
    genre_data = api_call(url, access_token)
    
    if genre_data:
        all_genre_data[genre] = genre_data
        print(f"Dados para o gênero '{genre}' adicionados.")

# Salvar todos os dados em um único arquivo JSON
with open('spotify_data.json', 'w') as f:
    json.dump(all_genre_data, f, indent=2)

print("Todos os dados salvos em spotify_data.json")
