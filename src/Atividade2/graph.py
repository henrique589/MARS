import matplotlib.pyplot as plt
import networkx as nx
import json

# Carregar dados do JSON
with open('spotify_data.json', 'r') as f:
    data = json.load(f)

# Inicializar o grafo
G = nx.Graph()

# Definir os gêneros a serem analisados
generos = ['rock', 'piano', 'jazz', 'pop', 'hip-hop']  # Alterar conforme a lista de gêneros

# Definir intervalos de popularidade
popularidade_intervals = {
    'Alta Popularidade': range(85, 101),
    'Média Alta': range(70, 85),
    'Média': range(50, 70),
    'Baixa Popularidade': range(0, 50)
}

# Montar a rede para cada faixa e artista (construção do grafo)
for genre in generos:
    if genre in data:  # Verificar se o gênero existe no JSON carregado
        print(f"Processando gênero: {genre}")
        for track in data[genre]['tracks']['items']:
            track_id = track['id']
            track_name = track['name']
            track_popularity = track['popularity']
            album_id = track['album']['id']
            album_name = track['album']['name']
            
            # Adicionar nó para a faixa com atributos
            G.add_node(track_id, label=track_name, type='track', popularity=track_popularity, album=album_name, genre=genre)
            
            # Adicionar nós e arestas para cada artista associado à faixa
            for artist in track['artists']:
                artist_id = artist['id']
                artist_name = artist['name']
                
                if artist_id not in G:
                    G.add_node(artist_id, label=artist_name, type='artist', genre=genre)
                
                # Conectar a faixa ao artista
                G.add_edge(track_id, artist_id)

            # Conectar faixas dentro do mesmo intervalo de popularidade
            for interval_name, interval_range in popularidade_intervals.items():
                if track_popularity in interval_range:
                    for other_track in data[genre]['tracks']['items']:
                        other_track_id = other_track['id']
                        if other_track_id != track_id and other_track['popularity'] in interval_range:
                            G.add_edge(track_id, other_track_id)

# Cálculo das Propriedades Básicas
degree_distribution = [val for (node, val) in G.degree()]
clustering_coefficient = nx.average_clustering(G)
num_vertices = G.number_of_nodes()
num_edges = G.number_of_edges()

print(f"Número de vértices: {num_vertices}")
print(f"Número de arestas: {num_edges}")
print(f"Coeficiente de clustering médio: {clustering_coefficient}")
print(f"Distribuição de graus: {degree_distribution}")

# Calcular Centralidades
degree_centrality = nx.degree_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Adicionar centralidades como atributos nos nós
for node in G.nodes():
    G.nodes[node]['degree_centrality'] = degree_centrality[node]
    G.nodes[node]['eigenvector_centrality'] = eigenvector_centrality[node]

# Plotar a Rede com Tamanho dos Vértices Proporcional à Centralidade
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)
node_sizes = [1000 * eigenvector_centrality[node] for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="green", alpha=0.7)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=8)

plt.title("Grafo de Músicas e Artistas - Spotify (Gêneros Múltiplos)")
plt.axis("off")
# Salvar a imagem antes de mostrar
plt.savefig("grafo_spotify.png", format="png", dpi=300, bbox_inches="tight")  # Ajuste o formato e dpi conforme necessário
plt.show()
