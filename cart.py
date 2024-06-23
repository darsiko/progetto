from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from models import Cart, CartItem, Product

cart_blueprint = Blueprint('cart_blueprint', __name__, template_folder='templates', static_folder='static')


@cart_blueprint.route('/cart')
@login_required
def cart():
    return render_template('cart.html')



