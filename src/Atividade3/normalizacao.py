import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Utilizando os dados da base de dados
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Normalizar os dados
scaler = MinMaxScaler()
tracks_df[['track_duration_ms', 'track_popularity']] = scaler.fit_transform(
    tracks_df[['track_duration_ms', 'track_popularity']]
)

print(tracks_df.head()) 

# Fechar a conexão
conn.close()
