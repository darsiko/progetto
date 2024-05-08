from flask import Flask, render_template
import sqlalchemy as sq

app = Flask(__name__)

#username = postgres
#password = proprio nome
#nome_db = e_commerce

connection1 = 'postgresql://postgres:leonardo@localhost:5432/e_commerce'
connection2 = 'postgresql://postgres:dario@localhost:5432/e_commerce'
connection3 = 'postgresql://postgres:andrea@localhost:5432/e_commerce'

#per testare usare la propria connessione

engine = sq.create_engine(connection1, echo = True)

@app.route("/")
def index():
    con = engine.connect()
    con.commit()
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():

    return render_template('register.html')

@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
