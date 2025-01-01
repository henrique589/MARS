import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Carregar dados da tabela Tracks
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Selecionar colunas numéricas para clustering
numeric_columns = ['track_duration_ms', 'track_popularity']
data = tracks_df[numeric_columns].dropna()

# Normalizar os dados
scaler = StandardScaler()
normalized_data = scaler.fit_transform(data)

# Aplicar K-Means com 3 clusters (n_clusters pode ser ajustado)
kmeans = KMeans(n_clusters=3, random_state=42)
data['cluster'] = kmeans.fit_predict(normalized_data)

# Adicionar os clusters ao DataFrame original
tracks_df['cluster'] = data['cluster']

# Visualizar os clusters
plt.figure(figsize=(10, 8))
sns.scatterplot(x=data['track_duration_ms'], y=data['track_popularity'], hue=data['cluster'], palette="viridis")
plt.title("Clusters de Músicas (K-Means)")
plt.xlabel("Duração (ms)")
plt.ylabel("Popularidade")
plt.legend(title="Cluster")
plt.show()

# Fechar a conexão com o banco de dados
conn.close()