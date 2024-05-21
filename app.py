import route
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import *
from flask_sqlalchemy import SQLAlchemy
from requests import auth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
import re

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'ubersecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/e_commerce'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    address = db.Column(db.String(80))
    role = db.Column(db.String(80))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    var = current_user.is_authenticated
    return render_template('index.html', var=var)


@app.route('/private', methods=['GET', 'POST'])
def private():
    return render_template('private.html', current=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(User).filter_by(email=email).first()
        remember = True if request.form.get('remember') else False

        if user is not None:
            if user.role == 'admin' and password == 'pass123' and email == "admin@admin":
                login_user(user, remember=remember)
                return redirect(url_for('admin'))
            if user.check_password(password):
                login_user(user, remember=remember)
                return redirect(url_for('index'))
            else:
                error = 'Invalid credentials'
                return internal_error(error)
        else:
            error = 'User not found'
            return internal_error(error)

    return render_template('login.html')



@app.errorhandler(500)
@app.errorhandler(400)
def internal_error(error):
    return render_template('errore.html', error=error)


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
        name = request.form['name']
        email_register = request.form['email']
        password = request.form['password']
        address = request.form['address']
        role = request.form.get('select')
        users = User(name=name, email=email_register, password=password, role=role)
        users.set_password(password)
        db.session.add(users)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "admin@admin" and password == "pass123":
            return redirect('/admin')
        else:
            error = 'Invalid credentials'
            return internal_error(error)

    return render_template('admin_login.html')


@app.route('/product')
def product():
    return render_template('product.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/products')
def products():
    return render_template('products.html')
