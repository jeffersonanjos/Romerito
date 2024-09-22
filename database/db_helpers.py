import sqlite3

def get_connection():
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.sqlite')
    # Configurar o row_factory para usar sqlite3.Row
    conn.row_factory = sqlite3.Row
    return conn