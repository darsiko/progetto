from flask import Blueprint, render_template
from models import Product

products_bp = Blueprint('products_bp', __name__, template_folder='templates', static_folder='static')


@products_bp.route('/products')
def list():
    return render_template('products/products.html')


@products_bp.route('/product')
def view(product_id):
    return render_template('products/product.html')
