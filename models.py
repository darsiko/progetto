from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ubersecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = 'postgresql://postgres:postgres@localhost:5433/e_commerce'
app.config['SQLALCHEMY_DATABASE_URI'] = conn

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
engine = create_engine(conn)
Session = sessionmaker(bind=engine)
session = Session()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    address = db.Column(db.String(80))
    role = db.Column(db.String(80))

    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)
    cart = db.relationship('Cart', uselist=False, backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def __init__(self, name, email, password, address, role):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def email_already_used(email):
        return User.query.filter_by(email=email).first() is not None

    @staticmethod
    def name_already_used(name):
        return User.query.filter_by(name=name).first() is not None


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    amount = db.Column(db.Integer)
    price = db.Column(db.Float)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    orders = db.relationship('Order', backref='ordered_product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    product_categories = db.relationship('ProductCategory', backref='product', lazy=True)

    def __init__(self, name, description, amount, price, seller_id):
        self.name = name
        self.description = description
        self.amount = amount
        self.price = price
        self.seller_id = seller_id


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    state = db.Column(db.String(80))
    total = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, date, state, total, user_id, product_id, quantity):
        self.date = date
        self.state = state
        self.total = total
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

    def __init__(self, last_modified, user_id):
        self.last_modified = last_modified
        self.user_id = user_id


class CartItem(db.Model):
    __tablename__ = 'cart_item'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer)

    def __init__(self, product_id, cart_id, quantity):
        self.product_id = product_id
        self.cart_id = cart_id
        self.quantity = quantity


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)

    product_categories = db.relationship('ProductCategory', backref='category', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False, primary_key=True)

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, score, text, date, product_id, user_id):
        self.score = score
        self.text = text
        self.date = date
        self.product_id = product_id
        self.user_id = user_id
