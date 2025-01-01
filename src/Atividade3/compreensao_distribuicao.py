import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')

# Utilizando os dados da base de dados
tracks_df = pd.read_sql_query("SELECT * FROM Tracks", conn)

# Selecionar apenas colunas numéricas
numeric_columns = tracks_df.select_dtypes(include=['float64', 'int64'])

# Calcular a matriz de correlação
corr = numeric_columns.corr()

# Plotar o heatmap da matriz de correlação
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlação")
plt.show()

# Fechar a conexão
conn.close()