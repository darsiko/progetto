from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import re

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'ubersecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:psw123@localhost:5432/postgres'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# @login_manager.user_loader
# def load_user(user_id):
#    with Session(engine) as session:
#        return session.get(User, user_id)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    #    if current_user.is_authenticated:
    #        return redirect(url_for('private'))
    return render_template('index.html')


@app.route('/private', methods=['GET', 'POST'])
#@login_required
def private():
    return render_template('private.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if password != user.password and email != user.email:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
#@login_required
def logout():
    #logout_user()
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
        name = request.form['username']
        email_register = request.form['email']
        password = request.form['password']
        role = request.form.get('select')
        users = User(name, email_register, password, role)
        db.session.add(users)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/admin-login')
def login_admin():
    return render_template('admin-login.html')
