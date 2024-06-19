from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from models import ShoppingCart, CartItem, Product, db

cart_blueprint = Blueprint('cart_blueprint', __name__, template_folder='templates', static_folder='static')


@cart_blueprint.route('/cart')
@login_required
def cart():

    return render_template('cart.html')


