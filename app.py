from flask import Flask, render_template
import sqlalchemy as sq
import re

app = Flask(__name__)

connection = 'postgresql://postgres:psw123@localhost:5431/postgres'
engine = sq.create_engine(connection, echo=True)

@app.route("/")
def index():
    engine.connect()
    engine.commit()
    engine.close()
    return render_template('index.html')


@app.route('/login')
def login():

    return render_template('login.html')

def check_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.search(pattern, email):
        return True
    else:
        return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        con = engine.connect()
        con.execute(sq.insert().values(username=username, email=email, password=password))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('register.html')

@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
