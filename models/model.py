from flask_login import UserMixin
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_helpers import get_connection

class User (UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def save(username, password):
        password_hash = generate_password_hash(password)
        conn = get_connection()
        cursor = conn.cursor()
        sql = 'INSERT INTO user (username, password) VALUES (?,?)'
        cursor.execute(sql, (username, password_hash))
        conn.commit()
        conn.close()

    def select(username, password):
        conn = get_connection()
        cursor = conn.cursor()

        # Consulta para buscar o usuário pelo nome de usuário
        sql = 'SELECT * FROM user WHERE username = ?'
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        conn.close()

        # Depuração
        print(f"User fetched from database: {user}")

        if user:
            print(f"Username: {user['username']}, Password Hash: {user['password']}")
            
        # Verifica se o usuário foi encontrado e se a senha está correta
        if user and check_password_hash(user['password'], password):
            user_id = user['id']
            session['user_id'] = user_id
            return user_id
        return None

