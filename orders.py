import datetime
from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from sqlalchemy import func
from sqlalchemy.orm import aliased

from models import Order, Cart, CartItem, Product

orders_blueprint = Blueprint('orders_blueprint', __name__, template_folder='templates', static_folder='static')


@orders_blueprint.route('/orders')
def orders():
    order = Order.query.filter_by(user_id=current_user.id)
    return render_template('orders.html', orders=order)


@orders_blueprint.route('/orders/<int:idx>', methods=["GET", "POST"])
def add_order(idx):

    return redirect(url_for('orders_blueprint.orders'))
