from flask import Blueprint, render_template
from flask_login import current_user

from models import Product

products_bp = Blueprint('products_bp', __name__, template_folder='templates', static_folder='static')


@products_bp.route('/products')
def list():
    return render_template('products.html', current_user=current_user)


@products_bp.route('/product')
def view(product_id):
    return render_template('product.html')


