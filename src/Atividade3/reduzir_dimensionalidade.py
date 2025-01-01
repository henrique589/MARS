import pandas as pd
import sqlite3
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Carregar dados da tabela Tracks
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Selecionar apenas colunas numéricas para redução de dimensionalidade
numeric_columns = ['track_duration_ms', 'track_popularity']
data_to_reduce = tracks_df[numeric_columns].dropna()

# Normalizar os dados antes de aplicar PCA
scaler = StandardScaler()
normalized_data = scaler.fit_transform(data_to_reduce)

# Aplicar PCA para reduzir a 2 dimensões
pca = PCA(n_components=2)
reduced_data = pca.fit_transform(normalized_data)

# Criar DataFrame com os componentes principais
reduced_df = pd.DataFrame(reduced_data, columns=['PC1', 'PC2'])

# Visualizar a contribuição de cada componente
print("\nContribuição de variância explicada por componente:")
print(pca.explained_variance_ratio_)

# Adicionar os clusters ao DataFrame original (se necessário)
tracks_df['PC1'] = reduced_df['PC1']
tracks_df['PC2'] = reduced_df['PC2']

# Visualizar a projeção 2D
plt.figure(figsize=(8, 6))
sns.scatterplot(x='PC1', y='PC2', data=reduced_df)
plt.title("Projeção PCA (2 Componentes Principais)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# Fechar a conexão com o banco de dados
conn.close()