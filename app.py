from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from database.db_helpers import get_connection
from models.model import User
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superdificil'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'jeffinbonitin@gmail.com'
app.config['MAIL_PASSWORD'] = 'dpcu movp vzrg rkzt'

mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'SELECT * FROM user WHERE id = ?'
    cursor.execute(sql, (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(row['id'], row['username'], row['password'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['nome']
        password = request.form['senha']
        
        print(f"Trying to log in with username: {username}")

        user_id = User.select(username, password)

        if user_id:
            print(f"User ID found: {user_id}")
            user = User(user_id, username, None)  # Cria um usuário com ID retornado
            login_user(user)
            return redirect(url_for('dash'))
        else:
            print("Login failed: invalid username or password.")
            return 'ERRO'
            # login_user(user)
            # return redirect(url_for('dash'))
        # else:
        #     flash('Nome de usuário ou senha inválidos.')
        #     return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['nome']
        password = request.form['senha']

        User.save(username, password)
        flash('Usuário registrado com sucesso!')
        return redirect(url_for('login'))

@app.route("/create_database")
def create_database():
    db = 'database.sqlite'
    schema = 'database/schema.sql'
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    with open(schema, 'r') as banco:
        schema_sql = banco.read()
        cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    return 'Banco de dados criado com sucesso!'

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/email', methods=['POST','GET'])
def email():
    if request.method == 'GET':
        return render_template ('email.html')
    else:
        user_email = request.form['email']
    
        msg = Message("teste", sender="jeffinbonitin@gmail.com", recipients=[user_email])
        msg.body = "Albion online é um MMO RPG sandbox."
        msg.html = "<b>receba.</b>"
        
        
        with app.app_context():
            mail.send(msg)
        
        return "Email enviado com sucesso!"   

if __name__ == '__main__':
    app.run(debug=True)
