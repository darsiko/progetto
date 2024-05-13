from flask import Flask, render_template, request, redirect
import sqlalchemy as sq
import re

app = Flask(__name__)
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)

connection = 'postgresql://postgres:psw123@localhost:5432/postgres'

engine = sq.create_engine(connection, echo=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    engine.connect()
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
        print(username)
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('select')
        con = engine.connect()
        con.execute(sq.text("INSERT INTO users (a,b,c,d) VALUES (username,email,password,role)"))
        con.commit()
        con.close()
        return redirect('/login')
    return render_template('register.html')


@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
