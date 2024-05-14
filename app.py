from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_login import *
from requests import Session
import sqlalchemy as sq
import re
from sqlalchemy import select

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ubersecret'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, user, mail, pwd):
        self.id = id
        self.username = user
        self.email = mail
        self.password = pwd

@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        return session.get(User, user_id)

if __name__ == '__main__':
    app.run(debug=True)

connection = 'postgresql://postgres:leonardo@localhost:5432/e_commerce'
engine = sq.create_engine(connection, echo=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    engine.connect()
    if current_user.is_authenticated:
        return redirect(url_for('private'))
    return render_template('index.html')

@app.route('/private')
@login_required
def private():
    with Session(engine) as session:
        query = select(User)
        all_users = session.scalars(query)
        resp = make_response(render_template("private.html"))
    return resp

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        with Session(engine) as session:
            con = engine.connect()
            stmt = con.execute(sq.text("select * from users where Users.email == request.form['email'] and User.username == request.form['username'] and User.password == request.form['password']"))
            try:
                res = session.scalars(stmt).one()
                login_user(res)
                return redirect(url_for('private'))
            except sq.exc.NoResultFound:
                pass
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

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
