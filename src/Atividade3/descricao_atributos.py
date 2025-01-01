import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Utilizando os dados da base de dados
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Histograma de popularidade
sns.histplot(tracks_df['track_popularity'], bins=10, kde=True)
plt.title("Distribuição de Popularidade")
plt.show()

# Box-plot da duração
sns.boxplot(x=tracks_df['track_duration_ms'])
plt.title("Box-plot da Duração das Faixas")
plt.show()

# Fechar a conexao
conn.close()