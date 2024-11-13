import matplotlib.pyplot as plt
import networkx as nx
import json

# Carregar dados do JSON
with open('spotify_data.json', 'r') as f:
    data = json.load(f)

# Inicializar o grafo
G = nx.Graph()

# Definir os gêneros a serem analisados
generos = ['rock', 'piano', 'jazz', 'pop', 'hip-hop']

# Montar a rede apenas entre faixas do mesmo álbum
for genre in generos:
    if genre in data:  # Verificar se o gênero existe no JSON carregado
        print(f"Processando gênero: {genre}")
        
        # Agrupar faixas por álbum
        album_tracks = {}
        for track in data[genre]['tracks']['items']:
            album_id = track['album']['id']
            track_id = track['id']
            track_name = track['name']
            track_popularity = track['popularity']
            album_name = track['album']['name']
            
            # Adicionar nó para a faixa com atributos
            G.add_node(track_id, label=track_name, type='track', popularity=track_popularity, album=album_name, genre=genre)
            
            # Agrupar faixas pelo ID do álbum
            if album_id not in album_tracks:
                album_tracks[album_id] = []
            album_tracks[album_id].append(track_id)
        
        # Conectar faixas dentro do mesmo álbum
        for tracks in album_tracks.values():
            for i in range(len(tracks)):
                for j in range(i + 1, len(tracks)):
                    G.add_edge(tracks[i], tracks[j])

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

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="orange", alpha=0.7)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5)
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=8)

plt.title("Grafo de Faixas por Álbum - Spotify")
plt.axis("off")
# Salvar a imagem antes de mostrar
plt.savefig("grafo_faixas_album_spotify.png", format="png", dpi=300, bbox_inches="tight")
plt.show()
