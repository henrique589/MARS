import matplotlib.pyplot as plt
import networkx as nx
import json

# Carregar dados do JSON
with open('spotify_data.json', 'r') as f:
    data = json.load(f)

# Inicializar o grafo
G = nx.Graph()

# Definir os intervalos de popularidade
popularidade_intervals = {
    'Alta Popularidade': range(85, 101),
    'Média Alta': range(70, 85),
    'Média': range(50, 70),
    'Baixa Popularidade': range(0, 50)
}

# Montar a rede (construção do grafo conforme descrito anteriormente)
for track in data['tracks']['items']:
    track_id = track['id']
    track_name = track['name']
    track_popularity = track['popularity']
    album_id = track['album']['id']
    album_name = track['album']['name']
    album_release_date = track['album']['release_date']
    
    G.add_node(track_id, label=track_name, type='track', popularity=track_popularity, album=album_name, release_date=album_release_date)
    
    for artist in track['artists']:
        artist_id = artist['id']
        artist_name = artist['name']
        
        if artist_id not in G:
            G.add_node(artist_id, label=artist_name, type='artist')
        
        G.add_edge(track_id, artist_id)
    
    for other_track in data['tracks']['items']:
        if other_track['album']['id'] == album_id and other_track['id'] != track_id:
            other_track_id = other_track['id']
            G.add_edge(track_id, other_track_id)

for interval_name, interval_range in popularidade_intervals.items():
    tracks_in_interval = [track['id'] for track in data['tracks']['items'] if track['popularity'] in interval_range]
    for i, track_id in enumerate(tracks_in_interval):
        for other_track_id in tracks_in_interval[i+1:]:
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
node_sizes = [1000 * eigenvector_centrality[node] for node in G.nodes()]  # Tamanho proporcional à centralidade de vetor próprio

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.7)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=8)

plt.title("Grafo de Músicas e Artistas - Spotify")
plt.axis("off")
plt.show()
