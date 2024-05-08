from flask import Flask, render_template
import sqlalchemy as sq

app = Flask(__name__)

connection = 'postgresql://postgres:leonardo@localhost:5432/e_commerce'

engine = sq.create_engine(connection, echo = True)

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
