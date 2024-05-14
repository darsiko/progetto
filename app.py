from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import *
from requests import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sq
import re

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ubersecret'

login_manager = LoginManager()
login_manager.init_app(app)

class User(sq.Model):
    id = sq.Column(sq.Integer, primary_key=True)
    username = sq.Column(sq.String(80))
    email = sq.Column(sq.String(80))
    password = sq.Column(sq.String(80))
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

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

@app.route('/private', methods=['GET', 'POST'])
@login_required
def private():
    return render_template('private.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        with Session(engine) as session:
            con = engine.connect()
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, email=email, password=password).first()
            if username != user.username and password != user.password and email != user.email:
                return redirect(url_for('login'))
    return render_template('login.html', username=username, email=email, password=password)

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
        if User.query.filter_by(username=username).first() is not None:
            flash('Username already exisxt.')
            return redirect(url_for('login'))
        user = User(username, email, password, role)
        sq.session.add(user)
        sq.session.commit()
        flash('Registretion successful!')
        return redirect('/login')
    return render_template('register.html')


@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
