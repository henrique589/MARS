import json
import sqlite3

# Carregar dados do JSON
with open('spotify_data.json', 'r') as f:
    data = json.load(f)

# Conectar ao banco de dados
conn = sqlite3.connect('spotify_data.db')
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Genres (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Artists (
    artist_id TEXT PRIMARY KEY,
    artist_name TEXT,
    artist_uri TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Albums (
    album_id TEXT PRIMARY KEY,
    album_name TEXT,
    album_release_date TEXT,
    album_type TEXT,
    total_tracks INTEGER,
    artist_id TEXT,
    FOREIGN KEY(artist_id) REFERENCES Artists(artist_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Tracks (
    track_id TEXT PRIMARY KEY,
    track_name TEXT,
    track_duration_ms INTEGER,
    track_popularity INTEGER,
    is_explicit BOOLEAN,
    album_id TEXT,
    genre_id INTEGER,
    FOREIGN KEY(album_id) REFERENCES Albums(album_id),
    FOREIGN KEY(genre_id) REFERENCES Genres(genre_id)
)
""")

# Inserir dados
for genre, genre_data in data.items():
    cursor.execute("INSERT OR IGNORE INTO Genres (genre_name) VALUES (?)", (genre,))
    genre_id = cursor.lastrowid

    for track in genre_data['tracks']['items']:
        # Inserir artistas
        artist = track['artists'][0]
        cursor.execute("""
        INSERT OR IGNORE INTO Artists (artist_id, artist_name, artist_uri)
        VALUES (?, ?, ?)
        """, (artist['id'], artist['name'], artist['uri']))

        # Inserir álbuns
        album = track['album']
        cursor.execute("""
        INSERT OR IGNORE INTO Albums (album_id, album_name, album_release_date, album_type, total_tracks, artist_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (album['id'], album['name'], album['release_date'], album['album_type'], album['total_tracks'], artist['id']))

        # Inserir faixas
        cursor.execute("""
        INSERT OR IGNORE INTO Tracks (track_id, track_name, track_duration_ms, track_popularity, is_explicit, album_id, genre_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (track['id'], track['name'], track['duration_ms'], track['popularity'], track['explicit'], album['id'], genre_id))

# Salvar e fechar conexão
conn.commit()
conn.close()
