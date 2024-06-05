from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ubersecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:leonardo@localhost:5432/e_commerce'

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)
db.init_app(app)

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

    def get(self):
        return self


class Product(db.Model, UserMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    price = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller = db.relationship('User', backref=db.backref('products', lazy=True))


class Order(db.Model, UserMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    state = db.Column(db.String(80))
    total = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))


class ShoppingCart(db.Model, UserMixin):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('shopping_cart', lazy=True))



class CartItem(db.Model, UserMixin):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('cart_item', lazy=True))
    amount = db.Column(db.Integer)


class Category(db.Model, UserMixin):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))


class ProductCategory(db.Model, UserMixin):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))


class Rewies(db.Model, UserMixin):
    __tablename__ = 'rewies'
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    text = db.Column(db.String(80))
    date = db.Column(db.Date)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('rewies', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('rewies', lazy=True))
