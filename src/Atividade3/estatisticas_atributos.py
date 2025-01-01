import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Utilizando os dados da base de dados
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Estatísticas descritivas
stats = tracks_df[['track_duration_ms', 'track_popularity']].describe()
print(stats)

# Fechar a conexao
conn.close()