from flask import Blueprint, render_template
from models import Product

products_bp = Blueprint('products_bp', __name__, template_folder='templates', static_folder='static')

@products_bp.route('/')
def list():
    products = Product.query.all()
    return render_template('products.html', products=products)

@products_bp.route('/')
def view(product_id):
    product = Product.query.get(product_id)
    return render_template('product.html', product=product)